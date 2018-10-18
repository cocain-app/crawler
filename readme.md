# Setting up
- Add links to the queue.txt file
- Create database.secret.sh file with the correct credentials
- Run docker container
  - docker build -t scraper .
  - docker run -v queue.txt:/app/queue.txt scraper
