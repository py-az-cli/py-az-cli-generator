PROJECTDIR=$(dirname $0)/..
cd $PROJECTDIR
source ./venv/bin/activate
python -m generate_code
cp output/pyaz $PROJECTDIR/py-az-cli/
