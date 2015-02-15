#!/bin/bash

sudo pip install -U virtualenv virtualenvwrapper

echo "#!/bin/bash" > ~/.bash_profile
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bash_profile
export WORKON_HOME=$HOME/.virtualenvs

if [ ! -d $WORKON_HOME ]
then
    mkdir $WORKON_HOME
fi

echo "source virtualenvwrapper.sh" >> ~/.bash_profile
echo "source $HOME/.bash_profile" >> ~/.bashrc