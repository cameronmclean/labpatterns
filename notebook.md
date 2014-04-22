labpatterns website notebook 
=======================

This is where I jot down all things peculiar to my learning and getting the whole thing set up...

CC-BY-3.0 unported license. Cameron McLean

###### 2014-04-21

using a mixture of eclipse with PyDev Django and adhoc text editors and terminals

#### Note: mySQL is installed at /Applications/mampstack...blah blah blah
####  and Python 2.7.2 is from anaconda installed at /Users/cameronmclean/anaconda... blah blah blah
### These are not typcial locations and many packages don't find the approprate libraries etc without some wrangling to env variables or PATH settings...

installed mysql-python libraries
`pip install mysql-python`
 needed to add `/Applications/mampstack/mysql/bin/` to `$PATH` to make `mysql_config` executable findable

Set mySQL backend in Django with the following in settings.py

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydb',
        'USER': 'root',
        'PASSWORD': 'bitnami',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

Next - created data schema using MySQLWorkbench
###### Because I have heard it is eaiser to do this then import it via `inspectdb` rather than build the model in Django first...
NOTE:
- foreign key constraints must have a unique name
- used `<tablename><column_name>_fk` syntax to name the constraint so the generated SQL looks something like 

```
-- -----------------------------------------------------
-- Table `mydb`.`force`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`force` (
  `force_name` VARCHAR(255) NOT NULL,
  `parent_pattern_name` VARCHAR(255) NOT NULL,
  `force_pictogram` MEDIUMBLOB NULL,
  `force_description` TEXT NULL,
  INDEX `pattern_name_idx` (`parent_pattern_name` ASC),
  PRIMARY KEY (`force_name`, `parent_pattern_name`),
  CONSTRAINT `force_parent_pattern_fk`
    FOREIGN KEY (`parent_pattern_name`)
    REFERENCES `mydb`.`design_pattern` (`pattern_name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
```

e.g the above is for the "force" relation. Note: DELETE/UPDATE are curently set to no action. Will revisit this later....
##### keep the table names in lowercase for import into Django.

#### Django only supports single column primary keys - these are needed for the admin interface - which I want to take advange of...
###### Going back to modify my ER for mySQL now... hmmm

###### 20140422

Modified schema to include single primary keys.
Used MySQLWorkbench to forward engineer basic pattern schema...
Using `mydb` as schema name.
OK!

Now - to autogenerate the models from the db schema, following the Django doc..
https://docs.djangoproject.com/en/1.6/howto/legacy-databases/

##### Python couldn't find `libmysqlclient.18.dylib`

added the following to ~/.bash_profile

```
# setting env variable for python-mysql to find all the things
DYLD_LIBRARY_PATH=$DYLD_LIBRARYPATH:/Applications/mampstack-5.4.26-2/mysql/lib
export DYLD_LIBRARY_PATH
```
Works now.

created models.py from db tables using 

```
$ python manage.py inspectdb > models.py
```

Cleaned up models.py by
1. Setting managed = True
2. Commenting out author model etc for now - just focus on the pattern structure
3. Changed order of model classes to resemnle correct/natural pattern format

synced db with no apps started yet (just an empty project with the models.py not yet moved to an app folder)

```
$ python manage.py syncdb
```

OK

*superuser* for site defined as
##### Username : cameronmclean
##### email : ca.mclean@auckland.ac.nz
##### psw : labpatterns

(for now - just for dev and testing on local machine of course!!)

Started app called **patterns**

```
$ python manage.py startapp patterns
```

moved cleaned up models.py into patterns app folder

added 'patterns' to the installed apps in the project settings.py

```
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'patterns',
)
```

added patterns to the admin.py in the pattern app

```
from patterns.models import *

admin.site.register(DesignPattern)
admin.site.register(Problem)
admin.site.register(Context)
admin.site.register(Solution)
admin.site.register(Force)
admin.site.register(Rationale)
admin.site.register(Diagram)
admin.site.register(Evidence)
```
to make all model objects able to managed by the admin site


