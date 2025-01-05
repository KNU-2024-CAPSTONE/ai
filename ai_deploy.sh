REPOSITORY=/home/ubuntu/repository
PROJECT_NAME=ai
PY_NAME=webApp.py

echo "> ai 배포 시작"

source $REPOSITORY/ai/venv/bin/activate

echo "> 기존 실행하던 파일 종료"
kill -9 $(pgrep -f $PY_NAME)

echo "> python 파일 실행"
cd $REPOSITORY/$PROJECT_NAME

# main 브랜치의 최신 내용 받기
echo "> Git Pull"
git pull origin main

nohup python webApp.py > $REPOSITORY/ai.log > $REPOSITORY/$PROJECT_NAME.log 2>&1 &
