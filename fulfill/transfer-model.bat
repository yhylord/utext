@echo off
gcloud compute scp --recurse ./qa_net/train/* utext@utext-elasticsearch:/home/utext/utext/fulfill/qa_net/train
gcloud compute scp --recurse ./qa_net/data/* utext@utext-elasticsearch:/home/utext/utext/fulfill/qa_net/data
pause