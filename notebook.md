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

## Using an exising mySQL to autogenreate the model wasn't so good

All sorts of niggly little things, like only primary keys can autoupdate, field mismatches 
eg - I had declared pictogram fields as MEDIUMBLOB, but Django doesn't like this - prefers ImageField or FileField, which are stored as VARCHAR and point to the path of the stored image on the webserver 
##### So images for now might not be stored in the db... will chase this up later...

### Re-wrote the models.py from a Django first persective, and overide the default table naming mechanism.
Deleted the database using mySQLWorkbench, created a new one with the same name `mydb`
ran 
`$ python manage.py syncdb`
Needed to issue a new superuser via
`$ python manage.py createsuperuser` (used the same credential as above)

Typical classes for the model (in models.py) now look like this

```
class Force(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Name', unique=True, max_length=255)
    parent_pattern = models.ForeignKey(DesignPattern)
    pictogram = models.ImageField('Force Pictogram', upload_to='pictograms')
    description = models.TextField('Description', blank=True)
    
    def __unicode__(self):
        return self.parent_pattern.name

    class Meta:
        db_table = 'force'
```
-Allows autogen on ID field, which the primary key - makes Admin site nicer
- will prbably need to tweak the unicode(self) return later...

In testing - db constraints seem to work - cant add force without it belonging to a parent pattern.
Nice.

I'm liking this for now !

OK - 
### Dealing with changes to DB/Model Schema

So it seems that Django is OK to add new models (i.e classes/db tables), but making chages to exisitng ones and keeping it in sync with the DB is troublesome. i.e if you later want to make a field unique=true

So I installed South and followed their documentation http://south.readthedocs.org/en/latest/tutorial/part1.html
`$ pip install South`
Added `'south'` to the installed apps in settings.py
Ran `syncdb`
then ran `$ python manage.py convert_to_south patterns` to convert the exisitng app so that model changes are more eaisily handled and synced with the DB.

Havent needed to use it yet, but internets say it's useful/essential...

###### 20140423

Added example pattern to db via Django admin page.
Admin page and model needs *much* tweaking, but first aim is just to have something there so we can see if R2RML and various engines can get it out and into RDF...

wrote simple R2RML file to get pattern names from db and turn them into Classes, with an IRI and a rdfs:label.

Now - to install DB2Triples

1. Install maven

- alrady installed via Xcode.
Following http://books.sonatype.com/mvnref-book/reference/installation-sect-maven-install.html

Created symbolic link so other apps can find it and then added evn variable and PATH settings

```
/usr/local $ ln -s apache-maven/apache-maven-3.2.1 mavan
/usr/local $ export M2_HOME=/usr/local/maven
/usr/local $ export PATH=${M2_HOME}/bin:${PATH}
```

mvn works OK.

Next - cloned db2triples from https://github.com/antidot/db2triples
cd into cloned dir and ran `mvn package`
which takes the pom.xml and does some magic to create db2triples-1.0.3-SNAPSHOT.jar

db2triples has some dependancies 
 
downloaded -

apache commons CLI from http://commons.apache.org/proper/commons-cli/download_cli.cgi
and cp commons-cli-1.2.jar into `target` dir

apache common-logging 1.1.1 from http://archive.apache.org/dist/commons/logging/binaries/
and cp commons-logging-1.1.1.jar into `target` dir

OPenRDF Sesame 2.6.10 from http://sourceforge.net/projects/sesame/files/Sesame%202/
and cp openrdf-sesame-2.6.10-onejar.jar into `target` dir

also got mySQL JDBC driver from http://dev.mysql.com/downloads/connector/j/
and cp mysql-connector-java-5.1.30-bin.jar into `target` dir

to run db2triples at the command line, we need to call net.antidot.semantic.rdf.rdb2rdf.main.Db2triples from db2triples-1.0.3-SNAPSHOT.jar
but also include all the dependencies...

I ended up doing it this way (with all the depedent .jar files in the same db2triples target dir)

Had to set `$ export CLASSPATH=/Users/cameronmclean/Projects/db2rml/target:$CLASSPATH` 
##### Note: no other path is set in CLASSPATH
-Probably should sort out proper PATH and CLASSPATH env variables for Java and maven... They dont seem to be configured....

But, running the following works!

```
java -cp commons-cli-1.2.jar:commons-logging-1.1.1.jar:openrdf-sesame-2.6.10-onejar.jar:db2triples-1.0.3-SNAPSHOT.jar:mysql-connector-java-5.1.30-bin.jar net.antidot.semantic.rdf.rdb2rdf.main.Db2triples 

```

##### Note: when connecting to DB via JDBC need to specify URL as "jdbc:mysql://127.0.0.1:3306/"

also had trouble with exception - `java.lang.NoClassDefFoundError: org.slf4j.LoggerFactory`
i.e cant find the class contained in slf4.jar 
added slf4j-api-1.7.7.jar from http://www.slf4j.org/download.html to `target` and included in depdency commandline list.

#### So... using a hastily scratched up R2RML.ttl file ...

Running

```
java -cp commons-cli-1.2.jar:commons-logging-1.1.1.jar:openrdf-sesame-2.6.10-onejar.jar:db2triples-1.0.3-SNAPSHOT.jar:mysql-connector-java-5.1.30-bin.jar:slf4j-api-1.7.7.jar net.antidot.semantic.rdf.rdb2rdf.main.Db2triples -b 'mydb' -l 'jdbc:mysql://127.0.0.1:3306/' -m 'r2rml' -p 'bitnami' -r 'lp_R2RML.ttl' -u 'root' -t 'RDFXML' -d 'com.mysql.jdbc.Driver' 
```
actaully worked to give an output.ttl (*note actually in RDF/XML* as per the -t )

Cool!

So - recap

- Configured maven
- Cloned db2triples git repo
- ran `mvn package` in cloned dir
- copied over additional .jar dependencies to db2triples target dir
- set $CLASSPATH
- run at command line as above - mostly seems OK!
 
 Note: maybe reorganise .jar in proper library places?

 ##### 20140429

copied slf4j-simple-1.7.7.jar into /target dir and added as dependency - removed LoggerFactory error....


```
java -cp commons-cli-1.2.jar:commons-logging-1.1.1.jar:openrdf-sesame-2.6.10-onejar.jar:db2triples-1.0.3-SNAPSHOT.jar:mysql-connector-java-5.1.30-bin.jar:slf4j-api-1.7.7.jar:slf4j-simple-1.7.7.jar net.antidot.semantic.rdf.rdb2rdf.main.Db2triples -b 'mydb' -l 'jdbc:mysql://127.0.0.1:3306/' -m 'r2rml' -p 'bitnami' -r 'lp_R2RML.ttl' -u 'root' -t 'RDFXML' -d 'com.mysql.jdbc.Driver' 
```
second version of r2rml.ttl file attempted to extract pattern names into a URI, and force names into a URI.
However - always received the following error

```
014/04/29 16:44:39:544 NZST [DEBUG] R2RMLEngine - [R2RMLEngine:constructLogicalTable] Run effective SQL Query : SELECT * FROM force
com.mysql.jdbc.exceptions.jdbc4.MySQLSyntaxErrorException: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'force' at line 1
```

Not sure why `pattern_name` works OK and `force` doesnt, but seems that db2triples doesnt pick the dbname properly.
Workaround for now seems that as long as I specify the db name prefix for all `rr:tableName "mydb.force"` etc it works...

So - spcify `<dn_name>.<table_name>` in r2rml files and seems OK.

Made a spiffy rule that turns force names into IRIs, asserts them as rdfs:Classes and then asserts them as partOf their parent pattern...

```
# Generate an IRI for each of the forces, and give them a label
<#TriplesMapForce> a rr:TriplesMap ;
    rr:logicalTable [ rr:tableName "mydb.force" ];

    rr:subjectMap [ rr:class rdfs:Class ;
                    rr:termType rr:IRI ;
                    rr:template "http://labpatterns.org/ns/force/{name}" ; 
                    ];

    rr:predicateObjectMap [ rr:predicate rdfs:label ;
                            rr:objectMap [ rr:column "name" ] ;
                            ];



# assert that each force is part of its parent pattern - does a join on id value form pattern and force tables, and return the value for the subject? for the #patternnaemtriplesmap above?

    rr:predicateObjectMap   [ rr:predicate odp:isPartOf ;
                            rr:objectMap [
                                rr:parentTriplesMap <#TriplesMapPatternName> ;
                                rr:joinCondition [
                                    rr:child "parent_pattern_id" ;
                                    rr:parent "id" ;
                                    ];
                                ];
                        ];.
```

seems to work! for exmaple the XML/RDF output has this kind of thing....

```
<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">

<rdf:Description rdf:about="http://labpatterns.org/ns/pattern/Photons%20Alive">
    <rdf:type rdf:resource="http://www.w3.org/2000/01/rdf-schema#Class"/>
    <label xmlns="http://www.w3.org/2000/01/rdf-schema#">Photons Alive</label>
</rdf:Description>

<rdf:Description rdf:about="http://labpatterns.org/ns/force/Immobilisation">
    <rdf:type rdf:resource="http://www.w3.org/2000/01/rdf-schema#Class"/>
    <label xmlns="http://www.w3.org/2000/01/rdf-schema#">Immobilisation</label>
</rdf:Description>

<rdf:Description rdf:about="http://labpatterns.org/ns/force/Immobilisation">
    <isPartOf xmlns="http://www.ontologydesignpatterns.org/cp/owl/partof.owl#" rdf:resource="http://labpatterns.org/ns/pattern/Photons%20Alive"/>
</rdf:Description>

```

Cooool!

Next? > to put this .rdf into a triplestore/SPARQL endoint show that it can be accessed remotely and query it.
Then > build a proper Django/mySQL model and target 1)Meta Vocab, 2) Linked data version....
Then then > write the R2RML mappings.
Then then make the Django side have all the functions and look nice..  

##### 20140506

Havent attempted .rdf > SPAQRL yet, but did start on the pattern ontology - see other repo....

Building pattern site one step at a time.

Added view, url, and template for homepage, and a page to add new patterns.
Next to learn the django way of using forms to add objects to the DB....


