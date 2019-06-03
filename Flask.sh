#!/usr/bin/env bash

flaskEnv=${1:-$'development'}

export FLASK_APP=FlaskApp
export FLASK_ENV=${flaskEnv}

if [[ ${flaskEnv} == 'development' ]]
then
    export FLASK_DEBUG=1
elif [[ ${flaskEnv} == 'production' ]]
then
    export FLASK_DEBUG=0
fi

flask run
