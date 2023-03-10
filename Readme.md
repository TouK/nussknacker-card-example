### Running
- `cd docker; docker-compose up`
- Go to `http://localhost:8081`, create Nussknacker scenario and import `CardTransaction.json`            

### Sources of additional data
- https://iso20022.plus/2021/03/20/iso20022-api-2020-09-14/ 
- https://www.kaggle.com/datasets/dhanushnarayananr/credit-card-fraud (Public domain)
- https://www.kaggle.com/code/mattop/credit-card-fraud-classification-knn-dtree-rf/data (ASL 2.0)
- http://download.geonames.org/export/zip/PL.zip (CC BY 4.0)

### Contents
- `docker` contains modified Nussknacker quickstart (see e.g. `docker/nussknacker/nussknacker.conf`)
- `generator` - simple test data generator, 
- `schemas` - input/output schemas used 
- `geo` - localization database, based on Polish zip codes
- `model` - fraud detection model