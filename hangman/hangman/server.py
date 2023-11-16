import os
import os.path

import flask
from flask import Flask
from flask import request
from flask import abort
from flask import render_template, url_for, redirect
from flask import Blueprint, g, current_app, session
from markupsafe import escape
from werkzeug.middleware.proxy_fix import ProxyFix
import werkzeug.utils
from logging.config import dictConfig
import logging
import click
import pickle

from . import hangman


def create_app(instance_path=None):
  if instance_path is None:
    app = Flask(__name__, instance_relative_config=True)
  else:
    app = Flask(__name__, instance_relative_config=True,
                instance_path=instance_path)
    
  app.config.from_mapping(
    SECRET_KEY='DEV',
  )
  app.config.from_pyfile('config.py', silent=True)

  # Configure logging
  BASE_DIR = os.getcwd()
  log_file_name = os.path.join(BASE_DIR, 'server.log.txt')
  FORMAT = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
  logging.basicConfig(filename=log_file_name,
                      level=logging.INFO,
                      format=FORMAT,)
  

  # If so configured, setup for running behind a reverse proxy.
  if app.config.get('PROXY_CONFIG'):
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1,
                            x_host=1, x_prefix=1)
    logging.info("set proxy fix")

  try:
    logging.info("instance path = %s", app.instance_path)
    os.makedirs(app.instance_path)
  except OSError:
    pass

  app.register_blueprint(bp)

  @app.errorhandler(Exception)
  def handle_exception(e):
    logging.exception("Internal error")
    return e

  return app


bp = Blueprint('hangman', __name__, cli_group=None)


@bp.route('/.well-known/ai-plugin.json')
def serve_manifest():
  return flask.send_from_directory(current_app.root_path,
                                   'static/ai-plugin.json')

@bp.route('/openapi.json')
def serve_openapi():
  return flask.send_from_directory(current_app.root_path,
                                   'static/openapi.json')

@bp.route('/privacy')
def serve_privacy():
  return flask.send_from_directory(current_app.root_path,
                                   'static/privacy')


def load_game_record(game_id):
  file_name = game_id + ".pcl"
  file_path = os.path.join(current_app.instance_path, file_name)
  if not os.path.exists(file_path):
    return None

  f = open(file_path, 'rb')
  game = pickle.load(f) 
  f.close()
  return game

def save_game_record(game_id, game):
  file_name = game_id + ".pcl"  
  file_path = os.path.join(current_app.instance_path, file_name)
  # TODO: more unique tmp name
  f = open(file_path + '.tmp', 'wb')
  pickle.dump(game, f)
  f.close()
  os.replace(file_path + '.tmp', file_path)
  

@bp.route('/newgame')
def new_game():
  size = request.args.get('word_size', '9')
  max_wrong_guesses = request.args.get('max_wrong_guesses', '8')
  name = os.urandom(8).hex()
  logging.info("%s: new game [%s]: size=%s, guesses=%s",
               request.remote_addr, name, size, max_wrong_guesses)
  
  game = hangman.Game()  
  game.new_game(int(size), int(max_wrong_guesses))
  save_game_record(name, game)

  content = { "game_id" : name,
              "word" : game.word }
  return flask.jsonify(content)


@bp.route('/record_guess/<game_id>')
def record_guess(game_id):
  letter = request.args.get('letter')
  game_id = werkzeug.utils.secure_filename(game_id)

  logging.info("guess [%s]: letter=%s", game_id, letter)
  
  game = load_game_record(game_id)
  if game is None:
    return "Game not found", 400

  result = True
  if letter is not None:
    result = game.guess_letter(letter)
  save_game_record(game_id, game)

  game_state = game.get_game_state()
  if game_state.status == hangman.GAME_WON:
    status = "won"
  elif game_state.status == hangman.GAME_LOST:
    status = "lost"
  else:
    status = "inprogress"
  
  content = { "found" : result,
              "visible_word" : game_state.word,
              "word" : game.word,                
              "remaining_guesses" : game.guesses_remaining,
              "status" : status }
    
  return flask.jsonify(content)




