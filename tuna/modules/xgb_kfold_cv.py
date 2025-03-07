'''kfold_cv.KFoldCV

This module perform the k-fold cross validation using the sample passed trough the 
module configuration file. '''

from os import path
from pathlib import Path

import pandas as pd
from sklearn.model_selection import GridSearchCV, RepeatedStratifiedKFold

import xgboost as xgb
from xgboost import XGBClassifier

from tuna.utils.helpers import ModuleConfiguration, create_logger
from tuna.modules import Module
from tuna.utils.loaders import DatasetLoader

class XGBKFoldCV(Module):
    '''This module perform the k-fold cross validation using the sample passed trough the 
    module configuration file. '''

    __author__ = 'M Sotgia'
    __mail__ = 'mattia.sotgia@ge.infn.it'
    __version__ = 'v01_00_00'
    __date__ = 'mar 7th, 2025'

    def update(self):
        
        # 1. Initialize all ecessry steps
        self.configuration.default(path.expandvars('$TUNA_PATH/configurations/base/xgb_kfold_cv.json'))
        __config: ModuleConfiguration = self.configuration
        
        training_dataset_path: str = __config.get('training_dataset_path', required=True)

        output_path = __config.get('output_path', required=True)
        output_name = __config.get('output_name')

        # 2. Load all the data for training/testing and so on...
        dataset_string = path.join(training_dataset_path)
        loader = DatasetLoader.load_csv(
            dataset_string,
            equalize_populations=__config.get('equalize_classes'),
            split=__config.get('training_split'),
            shuffle=__config.get('shuffle_dataset')
        )

        signals = loader.features
        labels = loader.labels

        # 3. Define the parameter grids

        parameters_grid = {
            'learning_rate'     : __config.get('learning_rate', required=True),
            'min_split_loss'    : __config.get('min_split_loss', required=True),
            'max_depth'         : __config.get('max_depth', required=True),
            'min_child_weight'  : __config.get('min_child_weight', required=True),
            'max_delta_step'    : __config.get('max_delta_step', required=True),
            'colsample_bytree'  : __config.get('colsample_bytree', required=True),
            'colsample_bylevel' : __config.get('colsample_bylevel', required=True),
            'colsample_bynode'  : __config.get('colsample_bynode', required=True)
        }

        # 4. Define the CV k-folding

        estimator = XGBClassifier(objective='binary:logistic', verbosity=3, n_jobs=1)

        kfolds: list = __config.get('kfolds')
        n_splits, n_repeats = kfolds
        cv = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats)

        scoring = __config.get('scoring')
        n_jobs = __config.get('n_jobs', True)

        grid_search = GridSearchCV(estimator=estimator, param_grid=parameters_grid, cv=cv, scoring=scoring, n_jobs=n_jobs, verbose=5)
        grid_search.fit(signals, labels)
        cv_results_grid = grid_search.cv_results_
        
        results_df = pd.DataFrame(cv_results_grid)
        results_df.to_csv(Path(output_path, f'{output_name}.csv'))

        # print('The found best results are ')
        # print(grid_search.best_params_)
        # print('\n')
        # print(results_df)
 
