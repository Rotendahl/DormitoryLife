#/bin/bash
cd "$(dirname "${0}")"/. || exit 2
if ! [ -d backUps ]; then
    mkdir backUps
fi
cd backUps
heroku pg:backups:capture
heroku pg:backups:download
mv latest.dump $(date +"%Y%m%d_%H%M%S").dump
echo "Back up DormitoryDollares created"
exit
