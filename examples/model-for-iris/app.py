import subprocess
import logging
import time
import sys


PREDICTION_SOURCE = 'files/iris_data_test.csv'
PREDICTION_TARGET = 'files/irist_data_set_predict.csv'

log = logging.getLogger('auger.ai')


def dataset():
    print("Checking dataset...")
    dataset_list = (subprocess.check_output(
        'augerai dataset list', shell=True)
        .decode(sys.stdout.encoding)
        .splitlines())
    if len(dataset_list) == 1:
        print("No dataset found, creating the first...")
        subprocess.check_call('augerai dataset create', shell=True)
    else:
        checked = [x for x in dataset_list if x.startswith('[x]')]
        if len(checked):
            print("Found uploaded and selected dataset: %s" % checked[0])
        else:
            # no iris selected
            if filter(lambda x: x.endswith(' iris.csv'), dataset_list):
                print(
                    "Datasets found:"
                    "\n%s\n"
                    "selecting iris.csv." %
                    '\n'.join(dataset_list))
                subprocess.check_call(
                    'augerai dataset select iris.csv', shell=True)


def experiment():
    def do_wait(prompt):
        print(prompt)
        result = subprocess.run(
            'augerai experiment leaderboard', shell=True, stdout=subprocess.PIPE, check=False).stdout.decode(sys.stdout.encoding)
        if result.endswith('Search is completed.'):
            return result.splitlines()[-3].split('|')[0].strip()
        else:
            time.sleep(5)
            return do_wait('.')
    dataset()
    leaderboard = subprocess.run(
        ['augerai', 'experiment', 'leaderboard'],
        stdout=subprocess.PIPE, check=False).stdout.decode(sys.stdout.encoding)
    if not leaderboard.endswith('is  progress...'):
        subprocess.check_output('augerai experiment start', shell=True)
    return do_wait("Waiting for model to train...")


def deploy():
    model_id = experiment()
    print("Deploying model with id", model_id)
    subprocess.check_output(
        'augerai model deploy --locally %s' % model_id, shell=True)
    return model_id


def predict():
    deployed_model_id = deploy()
    if os.path.exists(PREDICTION_TARGET):
        print(
            "Prediction already exists."
            " If you want to re-run predict, just delete prediction file: " %
            PREDICTION_TARGET)
    else:
        subprocess.check_output(
            'augerai model predict -m %s --locally %s' % (
                deployed_model_id, PREDICTION_SOURCE
            ),
            shell=True)


def main():
    try:
        predict()
    except subprocess.CalledProcessError as e:
        import traceback; traceback.print_exc();
        print(
            "Example application execution has failed with error: '%s'" %
            str(e))


if __name__ == '__main__':
    main()