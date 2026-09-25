echo "Creating dev and test branches..."  
git checkout -b dev  
git checkout -b test  
 git checkout main

echo "Initializing git repository..."  
git init  
git add .  
git commit -m "Initial commit: SERAI monorepo with  Aura.xlsx, AI, teleport scripts"  

GITHUB_USERNAME="Web4application" 
REPO_NAME="SERAI"   
GITHUB_URL=".  [https://github.com/web4hub/neomindmodel.git](https://github.com/Web4application/SERAI.git)"  
PYTHON_VERSION="3.11"  

git add .github/workflows/python.yml  
git commit -m "Add GitHub Actions CI workflow"  
git push origin main  
python3 -m http.server 8000 &
HTTP_PID=$!

trap 'kill "$HTTP_PID" 2>/dev/null || true' EXIT
