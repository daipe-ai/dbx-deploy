import setuptools
import shutil

BASE_DIR = 'src'

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='dbx-deploy',
    author='Jiri Koutny',
    author_email='jiri.koutny@datasentics.com',
    description='Databrics Deployment Tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DataSentics/dbx-deploy',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'dbx-deploy = DbxDeploy.DeployerCommand:DeployerCommand.run',
            'dbx-deploy-submit-job = DbxDeploy.DeployerJobSubmitterCommand:DeployerJobSubmitterCommand.run',
            'dbx-deploy-with-cleanup = DbxDeploy.DeployWithCleanupCommand:DeployWithCleanupCommand.run',
            'dbx-delete-all-jobs = DbxDeploy.JobsDeleterCommand:JobsDeleterCommand.run',
        ],
    },
    packages=setuptools.find_namespace_packages(where=BASE_DIR),
    package_data={
        '': ['*.yaml', '*.tpl']
    },
    package_dir={'': BASE_DIR},
    install_requires=[
        'injecta>=0.4.0',
        'nbconvert',
        'dbx-notebook-exporter',
        'python-box',
        'databricks-api',
        'requirements-parser'
    ],
    version='0.3.3',
    script_args=['bdist_wheel']
)

shutil.rmtree('build')
shutil.rmtree('src/dbx_deploy.egg-info')
