TARGET=/srv/www/nueleanu-discussion
PIPELINE=/srv/www/nueleanu-discussion-pipeline

mkdir -p $TARGET

if [ ! -d $PIPELINE ]; then
  git clone https://github.com/MihaiNueleanu/blog-discussion $PIPELINE
else
  cd $PIPELINE
  git pull
fi

cd $PIPELINE

[ $(cat previous-version.txt 2> /dev/null) ] && PREVIOUS=$(cat previous-version.txt) || PREVIOUS='NULL'
CURRENT=$(git rev-parse HEAD)

echo 'PREVIOUS VERSION --> '$PREVIOUS;
echo 'CURRENT VERSION --> '$CURRENT;

if [ $CURRENT != $PREVIOUS ]; then
  poetry config virtualenvs.in-project true
  poetry install

  cp -a . $TARGET

  cd $TARGET
  source .venv/bin/activate
  pm2 start poetry run uvicorn main:app

  git rev-parse HEAD > previous-version.txt
fi

