from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

import mock
import shutil
import tempfile
import datetime

from .forms import EvaluationForm
from .models import *

# Create your tests here.
MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class Test_ML_Model(TestCase):
    def setUp(self):
        test_title = 'test_model'
        test_mock = mock.MagicMock(spec=File)
        test_mock.name = 'test_model.h5'
        my_model = ML_Model.objects.create(title=test_title, model_file=test_mock)

    @classmethod
    def tearDownClass(cls):
        def tearDownClass(cls):
            shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
            super().tearDownClass()

    def test_create_모델(self):
        test = ML_Model.objects.get(title='test_model')
        self.assertEqual(test.title, 'test_model')
        self.assertEqual(test.version, 1.0)
        self.assertEqual(test.date_published, datetime.date.today())

    def test_update_모델버전(self):
        test = ML_Model.objects.get(title='test_model')
        old_version = test.version
        test.version = 1.2

        test.save()

        test = ML_Model.objects.get(title='test_model')
        self.assertNotEqual(test.version, old_version)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class Test_Evaluate(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        test_title = 'test_model'
        test_mock = mock.MagicMock(spec=File)
        test_mock.name = 'test_model.h5'
        my_model = ML_Model.objects.create(title=test_title, model_file=test_mock)


    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_create_evaluation(self):
        my_model = ML_Model.objects.get(pk=1)
        # my_eval = Evaluation.objects.create(ml_model=my_model)
        eval_data = {
            'total': 10,
            'success': 2,
        }
        print(eval_data)
        form = EvaluationForm(data=eval_data, instance=my_model) #, instance=my_eval)
        form.save()
        print(">>>", my_model.evaluation)
        self.assertTrue(form.is_valid())


    def test_update_evaluation(self):
        my_model = ML_Model
        # form =
        eval_data = {
            'total': 10
        }
