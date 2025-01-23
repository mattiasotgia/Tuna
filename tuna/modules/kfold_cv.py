'''kfold_cv.KFoldCV

This module perform the k-fold cross validation using the sample passed trough the 
module configuration file. '''

from os import path
from pathlib import Path

import pandas as pd
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import GridSearchCV, RepeatedStratifiedKFold
from sklearn.tree import DecisionTreeClassifier

from tuna.utils.helpers import ModuleConfiguration, create_logger
from tuna.modules import Module
from tuna.utils.loaders import DatasetLoader

class KFoldCV(Module):
    '''This module perform the k-fold cross validation using the sample passed trough the 
    module configuration file. '''

    __author__ = 'M Sotgia'
    __mail__ = 'mattia.sotgia@ge.infn.it'
    __version__ = 'v01_01_02'
    __date__ = 'jan 22nd, 2025'

    def update(self):
        
        # 1. Initialize all ecessry steps
        self.configuration.default(path.expandvars('$TUNA_PATH/configurations/base/kfold_cv.json'))
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
            'estimator__max_depth'             : __config.get('estimator__max_depth', required=True),
            'estimator__min_impurity_decrease' : __config.get('estimator__min_impurity_decrease', required=True),
            'estimator__min_samples_split'     : __config.get('estimator__min_samples_split', required=True),
            'estimator__min_samples_leaf'      : __config.get('estimator__min_samples_leaf', required=True),
            'estimator__ccp_alpha'             : __config.get('estimator__ccp_alpha', required=True),
            ## Only hardcoded parameter. JSON limitation
            'estimator__class_weight'          : [None], # __config.get('estimator__class_weight'), 
            'estimator__criterion'             : __config.get('estimator__criterion'),
            'n_estimators'                          : __config.get('n_estimators', required=True),
            'learning_rate'                         : __config.get('learning_rate', required=True),
            'algorithm'                             : __config.get('algorithm')
        }

        # 4. Define the CV k-folding

        estimator = AdaBoostClassifier(DecisionTreeClassifier())

        kfolds: list = __config.get('kfolds')
        n_splits, n_repeats = kfolds
        cv = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats)

        scoring = __config.get('scoring')
        n_jobs = __config.get('n_jobs', True)

        grid_search = GridSearchCV(estimator=estimator, param_grid=parameters_grid, cv=cv, scoring=scoring, n_jobs=n_jobs, verbose=5)
        grid_search.fit(signals, labels)
        cv_results_grid = grid_search.cv_results_

        # Still TODO: 
        #  - and maybe the ability to add some post-processing
        
        results_df = pd.DataFrame(cv_results_grid)
        results_df.to_csv(Path(output_path, f'{output_name}.csv'))

        # print('The found best results are ')
        # print(grid_search.best_params_)
        # print('\n')
        # print(results_df)
 
