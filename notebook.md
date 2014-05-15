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

1st tried making manual HTML forms... OK
2nd - tried the Django forms library - OK but looks terrible on screen.
3rd - as the forms map closely to the database - try ModelForm classes 
#### Hopefully it will be possible to customise the form HTML later 
- some prelim googleing suggests this is possible so will try for ModelForms for now.
Benefits of using Django forms is the ease of vaidation, cleaning, error handling etc....

##### 20140507

Alrighty - had much trouble getting modelforms to work with multiple fields for the DesignPattern model class.
trying to have a form for name entry (text) and pictogram (fileupload)
    Two important things I had to do.

    1. pass `request.FILES` to the form in dajango views.
    2. needed to add `enctype="multipart/form-data"` to the HTML template in the `<form>` attributes.

views.py now looks like

```
def add_new_pattern_name(request):
    form = NewPatternName()
    if request.method == 'POST':
        form = NewPatternName(request.POST, request.FILES)
        if form.is_valid():
            # model ImageField and modelForms field are causing validation errors. Need to declare the right type.. 
            form.save()
        
        return redirect('/')

    return render(request, 'new_name.html', {'form':form})
```

and new_name.html looks like

```
<html>
    <head>
        <title>Add a new design pattern</title>
    </head>
    <body>
        <form enctype="multipart/form-data" method="POST" action="">
            <table>
                {{ form.as_table }}
            </table>
            <input type="submit" value="Submit">
            {% csrf_token %}
        </form> 
    First web form goes here!
    Hopefully there is a form above....
    </body>
</html>
```

I can now save a pattern name and pictogram to the database via the web form...

NOTE: If pattern name is non-unique (i,e already exists - error passes silently, but the save to db does not occur)
Need to deal with this shortly...

#### Making links between Django pages

in the (HTML) template - specify the href attribute for links as `href="{% url <name> %}"` where `<name>` is the name attribute you gave in urls.py.
Note - this assumes linking pages between the same app - we can namespace this if we want to link pages across apps....

Next - after adding pic and name, redirect to new page to enter problem and context description.
-There is a problem here as we cant save any form input for problem or context without knowing the pattern ID - a foreign key in these tables in the DB.
Some possible solutions to investigate.
    maybe best is to not save the name/pictogram yet but commit and save to a variable.
    then do a GET-type of call on variable.pattern_ID

OK - so the essence of the problem is that I need to pass variables between views.
 - so that what is stored in page 1 is accessible to page 2 etc....

 There are a few ways to do this
    - cookies
    - GET from database and pass into hidden fields (dirties hte POST request?, and if interrupted half way through can leave incomplete db records)

AHh - maybe Django sessions is the way to go....
https://docs.djangoproject.com/en/dev/topics/http/sessions/#topics-http-sessions
eg use `newObject = form.save(commit=False)` and copy the various new pattern objects (models) to the session (server side db cache/cookie thing)
Once the chain and revision/editing is complete, write (`.save()`) all the objects to the db proper?

Ahh - but there is a problem - we dont get a primary key until the form/object is actuall saved in to the db.

Phew -OK - bad me - made many chnages without granualr commits or notes...

but - heres what I achieved/discovered today
0. I ended up saving the first pattern name and pictogram into the db before moving on the rest - this was pretty much unavoidable because of the way I set up primary/foreign key relationships.

1. use request.session to store arbitary data from views in a dict that can be accessed by other views/templates within the same browser session
    to access session variables within a *template* - use `{{ request.session.<key_name> }}` note that <key_name> is accessed via . notation here, not by typical `request.session['key_name']` as you would for a view
    #### note: i end up passing the image location and new name to the next page via session variales when it could in theory be retreived from the database. I chose this method so that each page a user is presented with depends on what they last entered, not what the last thing added to the db is....

    note: also - to use request.session data in templates i needed to add the following to settings.py - note the `django.core.context_processors.request`
    
    ```
    TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    )
    ``` 


2. changed model ImageFields to FileFields as imagefields do not support .svg (which we want)
    used `python manage.py schemamigration patterns --auto` followed by `python manage.py migrate` to make the change

3. had to figure out how to serve static, user-uplodaed image files - this was a pain 
    i did the following based on some stackexchange answers
    
to settings.py add

```
MEDIA_ROOT = "/Users/cameronmclean/Projects/eclipse_workspace/labpatterns/pictograms/"
MEDIA_URL = "/media/"
```

to urls.py add

```
url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
```

then - in templates when we want to display an image (remember the db stores the path to the image)

```
<img src="{{ MEDIA_URL}}path_to_file.xtn">
```

in my case - i used the session variable in the template to call the most recently added pictogram on the next page
the below renders the pattern name and pic entered on the last page to this new page 

```
<h1> {{ request.session.new_pattern_name }} </h1>
<p> <img src="{{ MEDIA_URL }}{{ request.session.new_pattern_image }}"> </p>

```

#### Note: media paths for serving static files need sorting - currently django only looks in .../pictograms but differnt models put them in various locations.... <note > now changed 20140512- all media is now in ...labpatterns/media/  with subdirs for js, pictograms, diagrams etc...


##### 20140509

dealing with the browser back button
- So there is a problem if the user is halfway through the series of pages and clicks back button to edit a previous form.
We need to keep the state and have django edit the instance of what was just added to the db rather than create a new one if one navigates back.

I manage this by storing the recently added form into into a session variable, before loading a form we check to to see if the variable exists - if it does, then load the form with the instance so that .save() will update it rather than create a new instance (this is how .save() works if handed an instance arguement). Ff a session variable (dict key) doesnt exist for this form - then just load as blank (i,e create new instance), and add the foreign key behind the scences from the info collected via the first form...
 So - for the first page - adding a new pattern - name and pictogram - we have

 ```
 # The first page to add a new pattern - after successful form submision it should redirect to adding problem and context
def add_new_pattern_name(request):
    form = NewPatternName()
    if request.method == 'POST':
        # check to see if we have added a pattern in this session (i.e user has clicked back on browser - if so, load that pattern to update rather than create a new one)
        # note we clear the session dictonary after the final form submission. 
        if 'new_pattern_key' in request.session:
            form = NewPatternName(request.POST, request.FILES, instance=DesignPattern.objects.get(id=request.session['new_pattern_key']))
        else: 
            form = NewPatternName(request.POST, request.FILES)
        # if form is valid save it to a new object, and store the object contents in session dictonary
        if form.is_valid():
            newPatternInstance = form.save()
            request.session['new_pattern_key'] = newPatternInstance.id
            request.session['new_pattern_name'] = newPatternInstance.name
            request.session['new_pattern_image'] = str(newPatternInstance.pictogram)

            return redirect('/newprobtext/')

          # print form.errors
    else:
        form = NewPatternName()
    return render(request, 'new_name.html', {'form':form})
```

#### note: this strategy requires us to delete all the session keys after the final form submission.
 
Oakie - 
Next up - added forms for forces.
We want multiple forms on one page, and the ability to dynamically add/delete extra forms.
tricky, but modelformset_factory seems to have it covered...
halfway throuhg learning/implementing this thingy...

one thing - the default for formset_factory is to query the model and present a form for each entry.... hmmm
need to overide this with `AuthorFormSet(queryset=Author.objects.none())` ...


##### 20140510

getting modelformsets to work was a PITA.
Mostly because I struggled to understand the documentation, and perhaps i'm doing thigns awkarly in my views/models/forms...

BUT - finally got one single - force form using the modelforms_factory to work.
##### note - it needs further testing - to see if the state and queryset is properly maintatined between pages.
also - next is to hook it into javascript to get dynamic 'add another force' buttons and forms. this will really check the looping over formset and assiging the proper foreign key (parent pattern)...

ALSO - side note - without thinking I had called a db table name "force" in my model - but of course this a reserved SQL word!!
pretty dumb - but fixed now so that table = `pattern_force` south migrations made it a doddle to fix/
*also note* that i needed to change the Meta details, not the class (model) name... as i'm using custom db table names....

```
class Force(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Name', unique=True, max_length=255)
    parent_pattern = models.ForeignKey(DesignPattern)
    pictogram = models.FileField('Force Pictogram', upload_to='pictograms')
    description = models.TextField('Description', blank=True)
    
    def __unicode__(self):
        return self.parent_pattern.name

    class Meta:
        db_table = 'pattern_force'
```

Back to the modelforms - getting at instances/objects for each form and setting the primary key (via the session variable) was eventaully done like this....

```
def add_new_force(request):
    ForceFormSet = modelformset_factory(Force, form=NewForce, can_delete=True)
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '',
    }
    if request.method == 'POST' :
        
        if 'forces_added' in request.session:
            formset = ForceFormSet(request.POST, request.FILES, data, queryset=Force.objects.get(parent_pattern=request.session['new_pattern_key']))
        
        else:
            formset = ForceFormSet(request.POST, request.FILES, data, queryset=Force.objects.none())
        
        if formset.is_valid():
            for form in formset.forms:
                newInstance = form.save(commit=False)
                newInstance.parent_pattern = DesignPattern.objects.get(id = request.session['new_pattern_key'])
                print dir(newInstance)
                print newInstance.description
                print newInstance.parent_pattern_id
                newInstance.save()  
#... and so on...
```

###NOTE - moving the `data` dict order in the ForeFormSet() call made all the difference - I had to make it come *after* request.POST and request.FILES or else the .save() doesn't work and saves an ampty string each time, which threw a DB integrity error (non-unique 'name' key) the second time through adding new pattern/forces....

OK - enough for now.

Play with dynamci adding/removing forms next...


##### 20140512

Dynamically adding force modelformset from the client side using javascript.
Not so easy to understand.
Ended up using this
http://blog.stanisla.us/2009/11/30/django-dynamic-formset-v1-1-released/
https://github.com/elo80ka/django-dynamic-formset

I cloned and copied the .js to .../labpatterns/media/js
also downloaded and copied in the lastest jQuery library http://jquery.com/download/ (v 1.11.1)

In the template needed to reference the js in the `<head>` as so...

```
<!DOCTYPE html>
<html lang=en>
    <head>
        <title>Use the force!</title>
        <link type="text/css" rel="stylesheet" href="{{ STATIC_URL }}base.css">
        <script type="text/javascript" src="{{ MEDIA_URL }}js/jquery-1.11.1.min.js"></script>
        <script type="text/javascript" src="{{ MEDIA_URL }}js/jquery.formset.js"></script>
        
    </head>
```

Then - modified the template for the form as so...

```
<body>
        <h1> {{ request.session.new_pattern_name }} </h1>
        <p> <img src="{{ MEDIA_URL }}{{ request.session.new_pattern_image }}"> </p>
        <form id="newForce" enctype="multipart/form-data" method="POST" action="">
            <div>
                {% for form in formset %}
                <p>
                    {{ form }}
                </p>
                {% endfor %}
            </div>
            <input type="submit" value="Submit">
            {% csrf_token %}
            {{ formset.management_form }}
                    
        </form> 
        <!-- this is the script to add another or remove an instance of the force formset.
        it uses a jQuery selector to select the form with #id newForce, and operates over the div element. 
        it doesnt seem to matter (for now! if i select just the <div> or the <p> within the <div> element. 
        difference is wheter it will be important later to incude the for loop or not. !-->
        <script type="text/javascript"> 
        $(function() {
            $('#newForce div p').formset();
        })
        </script>

    </body>
```
NOTE: - needed to add the `id='newForce'` attribute to the `<form>` element so the jQuery selecter can find it.
NOT sure about whether the js call should select before or after the for loop in the template - both seem to work for now...
ALSO - will need to figure out how to dynamically CSS style the add/remove links - they are functional for now, but ugly.

But all good - seems to be working.
NEXT is figure out how to keep the state / deal with the back button - this could be a major PITA... we'll see.
(note note : if dynamic forms and back browser back button is  pain - can try adding forces one at a time, with I'm done and save and add another buttons - using only Http functions...)

##### 20140513

Added Solution and Rationale views, urls, forms, template.
HAd heaps of trouble getting it to save to the db - because I copied the code from the Problem/context forms - AND FORGOT TO CHANGE THE MODELFORM to use the right model!
Duh!
Anyho workingnow...

Forces page - troube getting the forms to repopulate and load instance if browser back button is pressed.
This is because Firefox back button stores/caches pages itself and "back" returns you to the previous page in exactly the state you left it.
i.e it doesnt do a GET or reload. But i need it to do this properly reload all the form instances with the previously saved force data.
Otehrwise the forms are re-submitted as "new" forms/instances leading to extra (incorrect) froces being added to the pattern and db.
Tried many things
- decorating the add_forces view with
`@cache_control`
adding `<meta http-equiv="Cache-Control" content="no-store" />`
None of these worked...
What did work - at least for firefix is adding
`<body onunload="">` to the newforce.html template.

Perhaps forcing a page refresh on back is symptonmatic of larger flaws in my site nativation/flow design.
This may well be true, but for now - it's definately good enough.
ALSO - the same ideas I've been using to manage editing of exisitng forms on browser back can be reused to edit instances later on in the site design/evolution.

OK - back button issues with adding forced wasnt quite fixed.
When user hits back, the correct data is populated and edited, but also an extra blank form is added.
If not used this was storing a blank force in the db - bad.
Also - third time around or a second session - the blank force already exists and throws a db integrity error as cant have two forces with the same name.

Now modified the code to set modelfform_factory(extra=0) if reloading - this code comes before the if request.method == 'POST' (at the bottom)
but i have duplicated it again inside the first if - left it there from debugging - doesnt seem to do any harm but this is obviously a bad code smell and i'm doing something wrong....

But anyhoo - it works for now...


```
def add_new_force(request):
    ForceFormSet = modelformset_factory(Force, form=NewForce, can_delete=False)
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '',
    }
    if request.method == 'POST' :

        if 'forces_added' in request.session:
            ForceFormSet = modelformset_factory(Force, form=NewForce, can_delete=False, extra=0)
            data['form-TOTAL_FORMS'] = Force.objects.filter(parent_pattern=request.session['new_pattern_key']).count()
            initialForms = Force.objects.filter(parent_pattern=request.session['new_pattern_key'])
            print data['form-TOTAL_FORMS']
            print initialForms
            formset = ForceFormSet(request.POST, request.FILES, data, queryset=initialForms)
        

        else:
            formset = ForceFormSet(request.POST, request.FILES, data, queryset=Force.objects.none())
        
        if formset.is_valid():
            for form in formset.forms:
                newInstance = form.save(commit=False)
                newInstance.parent_pattern = DesignPattern.objects.get(id=request.session['new_pattern_key'])
        #       print dir(newInstance)
        #       print newInstance.description
        #       print newInstance.parent_pattern_id
                newInstance.save()  
                                
            request.session['forces_added'] = True

            return redirect('/newsolutionale/')
    else: 
        if 'forces_added' in request.session:
            ForceFormSet = modelformset_factory(Force, form=NewForce, can_delete=False, extra=0) # dont display extra forms if user hits back button
            data['form-TOTAL_FORMS'] = Force.objects.filter(parent_pattern=request.session['new_pattern_key']).count()
            initialForms = Force.objects.filter(parent_pattern=request.session['new_pattern_key'])
            print data['form-TOTAL_FORMS']
            print initialForms
            formset = ForceFormSet(queryset=initialForms)
        
        else:
            formset = ForceFormSet(queryset=Force.objects.none())

    return render(request, 'new_force.html', {'formset': formset})
```

##### 20140515

Took a break from entering pattern info into the db and played with thesaurus lookups for Force names.
The idea being that after one has entered a name for the Force, they are presented with simiarl or related terms, and can select a group of similar meanings. This short list can then be used to search against existing ontologies for exisiting formal concepts.
Ended up using http://words.bighugelabs.com/ and thier API.
Modifed a script from https://gist.github.com/hugorodgerbrown/3134709 to take string, parse it using space delim, submit the words one by one to the thesaurus, and crate a unified list of all similar, related or synomyn words for each word in the force term.
Did a hastly view/template/urls page just to get some output - seems to work OK.
The temporary view is `see_related_terms` which uses the `/related/` url and `see_related.html` template. 

Basic functions are there - next is to present the list as a choice and have the user shorten it...
  

