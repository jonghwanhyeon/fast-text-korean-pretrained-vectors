import logging
import fastText

dataset_filename = 'namuwiki_20170327_dataset'
model_filename = 'namuwiki_20170327_model'

pushover = {
    'token': '',
    'user': '',
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Training model...')
model = fastText.train_unsupervised(
    input=dataset_filename,
    dim=300,
    epoch=10
)

logger.info('Saving model...')
model.save_model(model_filename)

import subprocess
subprocess.call([ 'python3', '../notify.py', 'Done!' ])
