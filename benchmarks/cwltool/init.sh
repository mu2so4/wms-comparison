cd $(dirname "$0")

LOCKFILE="lockfile"

if [[ -f $LOCKFILE ]]; then
    echo "Init already complete. To init again remove the '$LOCKFILE' file"
    exit
fi

set -e

VENV_PATH=".cwltool-venv"

if [ ! -d $VENV_PATH ]; then
    echo "Creating the cwltool virtual environment..."
    python3.11 -m venv $VENV_PATH
else
    echo "The virtual environment already exists. Initialization of venv skipped."
fi


source $VENV_PATH/bin/activate
pip install -r ../../src/requirements.txt
pip install cwltool==3.1.20250110105449

touch $LOCKFILE

set +e

echo
echo "cwltool initialized successfully!"
echo
echo "Run it to run the pure workflow:"
echo "source $VENV_PATH/bin/activate"
echo "cwltool ../cwl/native/workflow.cwl params.yml"
echo
echo "Or"
echo "cwltool ../cwl/native/workflow_single_file.cwl params.yml"
