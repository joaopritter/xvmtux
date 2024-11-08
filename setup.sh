LIBPATH=~/.local/lib/xvmtux
BINPATH=~/.local/bin

if command -v python &>/dev/null; then
  PYTHON_CMD=python
elif command -v python3 &>/dev/null; then
  PYTHON_CMD=python3
else
  echo "Neither python nor python3 command found. Please install Python."
  exit 1
fi

if [ ! -d $LIBPATH ]; then
  echo "Creating .local folders..."
  if [ ! -d $BINPATH]; then
    mkdir $BINPATH
  mkdir $LIBPATH
  echo "Created necessary folders."
  echo "Moving app data..."
  cp -rf ./ $LIBPATH
  echo "Creating virtual environment..."
  $PYTHON_CMD -m venv $LIBPATH/.venv
  source $LIBPATH/.venv/bin/activate
  echo "Installing dependencies from requirements.txt..."
  pip install -r requirements.txt
  echo "Exiting virtual environment..."
  deactivate
  echo "Enabling execution permission for xvmtux..."
  chmod +x $LIBPATH/xvmtux
  echo "Adding executable to bin folder..."
  cp $LIBPATH/xvmtux $BINPATH

else
  echo "Updating app data..."
  cp -rf ./ $LIBPATH
  echo "Adding new dependencies from requirements.txt..."
  source $LIBPATH/.venv/bin/activate
  pip install -r requirements.txt
  echo "Exiting virtual environment..."
  deactivate
  echo "Updating executable in bin folder..."
  cp $LIBPATH/xvmtux $BINPATH
fi
