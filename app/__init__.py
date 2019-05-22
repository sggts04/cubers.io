""" Main initialization point of the web app. """

from flask import Flask
from flask_assets import Bundle, Environment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mobility import Mobility
from flask.logging import default_handler

from babel.dates import format_date

from slugify import slugify

from config import Config

import logging

from timber.formatter import TimberFormatter

# -------------------------------------------------------------------------------------------------

app = Flask(__name__)
app.config.from_object(Config)

Mobility(app)

app.secret_key = app.config['FLASK_SECRET_KEY']

DB = SQLAlchemy(app)
MIGRATE = Migrate(app, DB)

ASSETS = Environment(app)
ASSETS.register({
    'app_js': Bundle(
        'js/event_emitter.js',

        'js/util/time_convert_format.js',
        'js/util/extensions_and_polyfill.js',
        'js/util/handlebars_helpers.js',

        'js/controller/app_mode_manager.js',

        'js/timer.js',

        'js/controller/events_data_manager.js',
        'js/controller/current_scrambles_manager.js',
        'js/controller/user_settings_manager.js',

        'js/ui/solve_card_manager.js',
        'js/ui/timer_display_manager.js',
        'js/ui/scramble_display_manager.js',
        'js/ui/main_screen_manager.js',
        'js/ui/timer_screen_manager.js',
        'js/ui/scramble_image_generator.js',
        'js/ui/pentagons.js',

        'js/init.js',
        filters="jsmin",
        output='gen/app.js'
    ),

    'pentagons_js': Bundle(
        'js/ui/pentagons.js',
        filters="jsmin",
        output='gen/pentagons.js'
    ),

    'timer_desktop_css': Bundle(
        'less/common.less',
        'less/navbar.less',
        'less/timer/timer_common.less',
        'less/timer/desktop.less',
        filters="less,cssmin",
        output='gen/timer_desktop_css.css'),

    'timer_mobile_css': Bundle(
        'less/common.less',
        'less/navbar.less',
        'less/timer/timer_common.less',
        'less/timer/mobile.less',
        filters="less,cssmin",
        output='gen/timer_mobile_css.css'),

    'app_css': Bundle(
        'less/common.less',
        'less/navbar.less',
        'less/timer/timer_common.less',
        'less/timer/desktop.less',
        'less/timer/mobile.less',
        'less/events_page.less',
        'less/results.less',
        'less/user.less',
        'less/event_results.less',
        'less/settings.less',
        filters="less,cssmin",
        output='gen/app.css'),
})

# -------------------------------------------------------------------------------------------------

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(TimberFormatter())

app.logger.setLevel(logging.INFO)

app.logger.removeHandler(default_handler)
app.logger.addHandler(stream_handler)

# -------------------------------------------------------------------------------------------------

from app.tasks import *               # noqa

from app.persistence import models    # noqa
from app.routes.admin import *        # noqa
from app.routes.auth import *         # noqa
from app.routes.events import *       # noqa
from app.routes.home import *         # noqa
from app.routes.persistence import *  # noqa
from app.routes.results import *      # noqa
from app.routes.user import *         # noqa
from app.routes.util import *         # noqa
from app.commands import *            # noqa
from app.util.times import convert_centiseconds_to_friendly_time  # noqa

# -------------------------------------------------------------------------------------------------

@app.template_filter('slugify')
def slugify_filter(value):
    """ Jinja custom filter to slugify a string. """

    return slugify(value)


@app.template_filter('format_datetime')
def format_datetime(value):
    """ Jinja custom filter to format a date to Apr 1, 2018 format. """

    return format_date(value, locale='en_US')


@app.template_filter('friendly_time')
def friendly_time(value):
    """ Jinja custom filter to convert a time in cs to a user-friendly time. """

    try:
        converted_value = int(value)
    except ValueError:
        return value
    return convert_centiseconds_to_friendly_time(converted_value)


@app.template_filter('format_fmc_result')
def format_fmc_result(value):
    """ Jinja custom filter to convert a fake 'centisecond' result to FMC moves. """

    try:
        converted_value = int(value) / 100
    except ValueError:
        return value

    if converted_value == int(converted_value):
        converted_value = int(converted_value)

    return converted_value
