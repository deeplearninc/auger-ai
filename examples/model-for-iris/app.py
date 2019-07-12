import logging
import os
import subprocess
import sys
import time


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
    def do_wait(prompt=None):
        if prompt:
            print(prompt)
        result = (subprocess.run(
            'augerai experiment leaderboard',
            shell=True, stdout=subprocess.PIPE, check=False)
            .stdout.decode(sys.stdout.encoding))
        if 'Search is completed.' in result:
            return result.splitlines()[-3].split('|')[0].strip()
        else:
            time.sleep(5)
            return do_wait('.')
    dataset()
    leaderboard = subprocess.run(
        ['augerai', 'experiment', 'leaderboard'],
        stdout=subprocess.PIPE, check=False).stdout.decode(sys.stdout.encoding)
    if not 'is completed.' in leaderboard:
        print("Waiting for model to train...")
        subprocess.check_output('augerai experiment start', shell=True)
    else:
        print("Model is ready")
    return do_wait()


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
        result = (subprocess.run(
            'augerai model predict -m %s --locally %s' % (
                deployed_model_id, PREDICTION_SOURCE
            ),
            shell=True, stdout=subprocess.PIPE, check=False)
            .stdout.decode(sys.stdout.encoding))
        print(result)


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