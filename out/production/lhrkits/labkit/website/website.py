import os
import zipfile
import tempfile

from flask import Flask, render_template, abort, make_response
from werkzeug.contrib.atom import AtomFeed
from gridfs.errors import NoFile
from gridfs import GridFS
from bson.objectid import ObjectId
from werkzeug import secure_filename
from flask_mail import Mail
from flask_mail import Message

from flaskext.markdown import Markdown
from mdx_github_gists import GitHubGistExtension
from mdx_strike import StrikeExtension
from mdx_quote import QuoteExtension
from mdx_code_multiline import MultilineCodeExtension
import molecule
import user
import application
import pagination
import settings

from helper_functions import *


app = Flask('FlaskBlog')
md = Markdown(app)
md.register_extension(GitHubGistExtension)
md.register_extension(StrikeExtension)
md.register_extension(QuoteExtension)
md.register_extension(MultilineCodeExtension)
app.config.from_object('config')
mail = Mail(app)

#### gridfs server

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','zip','rar','tar.gz'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/files/<oid>')
def serve_gridfs_file(oid):
    try:
        file = FS.get(ObjectId(oid))
        # print file
        response = make_response(file.read())
        response.mimetype = file.content_type
        response.headers['Content-Disposition'] = 'attachment; filename=%s' % (file.filename)

        return response
    except NoFile:
        abort(404)

DB = app.config['DATABASE']
FS = GridFS(DB)


###


@app.route('/', defaults={'page': 1})
@app.route('/page-<int:page>')
def index(page):
    skip = (page - 1) * int(app.config['PER_PAGE'])
    # posts = postClass.get_posts(int(app.config['PER_PAGE']), skip)
    # count = postClass.get_total_count()
    # pag = pagination.Pagination(page, app.config['PER_PAGE'], count)
    # applicationClass.get_view('title','email')
    return render_template('index.html', default_settings=app.config, meta_title=app.config['BLOG_TITLE'])


## old molecule_list_routing
# @app.route('/molecule_list', defaults={'page': 1})
# @app.route('/molecule_list/page-<int:page>')
# def molecule_list(page):
#     skip = (page - 1) * int(app.config['PER_PAGE'])
#     posts = postClass.get_posts(int(app.config['PER_PAGE']), skip)
#     count = postClass.get_total_count()
#     pag = pagination.Pagination(page, app.config['PER_PAGE'], count)
#     return render_template('molecule_list.html', default_settings=app.config,posts=posts['data'], pagination=pag, meta_title=app.config['BLOG_TITLE'])


@app.route('/molecule_list', defaults={'page': 1})
@app.route('/molecule_list/page-<int:page>')
def molecule_list(page):
    skip = (page - 1) * int(app.config['PER_PAGE'])
    molecules = moleculeClass.get_molecules(int(app.config['PER_PAGE']), skip)
    count = moleculeClass.get_total_count()
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count)
    return render_template('molecule_list.html', default_settings=app.config,molecules=molecules['data'], pagination=pag, meta_title=app.config['BLOG_TITLE'])


@app.route('/tag/<tag>', defaults={'page': 1})
@app.route('/tag/<tag>/page-<int:page>')
def posts_by_tag(tag, page):
    skip = (page - 1) * int(app.config['PER_PAGE'])
    posts = postClass.get_posts(int(app.config['PER_PAGE']), skip, tag=tag)
    count = postClass.get_total_count(tag=tag)
    if not posts['data']:
        abort(404)
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count)
    return render_template('index.html', posts=posts['data'], pagination=pag, meta_title='Posts by tag: ' + tag)



@app.route('/application_is_successful/<title>')
def application_is_successful(title):
    molecule = moleculeClass.get_molecule_by_name(title)
    if not molecule['data']:
        abort(404)

    return render_template('application_is_successful.html',default_settings=app.config,molecule=molecule['data'], meta_title=app.config['BLOG_TITLE'] + '::' + molecule['data']['title'])

@app.route('/molecule/download/<title>')
def download_zip(title):


    archivefile = tempfile.mktemp()


    f = zipfile.ZipFile(archivefile,'w',zipfile.ZIP_DEFLATED)
    curdir=os.getcwd()
    os.chdir(moleculeClass.path)
    startdir = title
    for dirpath, dirnames, filenames in os.walk(startdir):
        for filename in filenames:
            if filename.find('~')==-1:
                f.write(os.path.join(dirpath,filename))

    os.chdir(curdir)
    f.close()
    try:
        file = open(archivefile,'r')
        # print file
        response = make_response(file.read())
        # response.mimetype = file.content_type
        response.headers['Content-Disposition'] = 'attachment; filename=%s' % (title+'.zip')

        return response
    except NoFile:

        abort(404)






@app.route('/molecule/<title>')
def single_molecule(title):
    # post = postClass.get_post_by_permalink(permalink)
    molecule = moleculeClass.get_molecule_by_name(title)
    if not molecule['data']:
        abort(404)
    # if post['data'].get('conformer'):
    #     file = FS.get(post['data']['conformer'])
    #     # print file
    #     # files = [FS.get_last_version(file) for file in FS.list()]
    #     # file_list = "\n".join(['<li><a href="%s">%s</a></li>' %
    #     #                        (url_for('serve_gridfs_file', oid=str(file._id)),
    #     #                         file.name)
    #     #                        for file in files])
    #     # file_list = " jojo"
    #     conformer = '<div>conformer display</div><img src="%s" height="220" width="220"/>' % (url_for('serve_gridfs_file', oid=str(file._id)))
    #     #
    # else:
    #     conformer=''
    # if post['data'].get('attachment'):
    #     file = FS.get(post['data']['attachment'])
    #     # print file
    #     # files = [FS.get_last_version(file) for file in FS.list()]
    #     # file_list = "\n".join(['<li><a href="%s">%s</a></li>' %
    #     #                        (url_for('serve_gridfs_file', oid=str(file._id)),
    #     #                         file.name)
    #     #                        for file in files])
    #     # file_list = " jojo"
    #     file_list = '<div>file for download</div><li><a href="%s">%s</a></li>' % (url_for('serve_gridfs_file', oid=str(file._id)),file.name)
    #     #
    # else:
    #     file_list=''
    return render_template('single_molecule.html',default_settings=app.config,molecule=molecule['data'], meta_title=app.config['BLOG_TITLE'] + '::' + molecule['data']['title'])
#
# @app.route('/molecule/<permalink>')
# def single_post(permalink):
#     post = postClass.get_post_by_permalink(permalink)
#     if not post['data']:
#         abort(404)
#     if post['data'].get('conformer'):
#         file = FS.get(post['data']['conformer'])
#         # print file
#         # files = [FS.get_last_version(file) for file in FS.list()]
#         # file_list = "\n".join(['<li><a href="%s">%s</a></li>' %
#         #                        (url_for('serve_gridfs_file', oid=str(file._id)),
#         #                         file.name)
#         #                        for file in files])
#         # file_list = " jojo"
#         conformer = '<div>conformer display</div><img src="%s" height="220" width="220"/>' % (url_for('serve_gridfs_file', oid=str(file._id)))
#         #
#     else:
#         conformer=''
#     if post['data'].get('attachment'):
#         file = FS.get(post['data']['attachment'])
#         # print file
#         # files = [FS.get_last_version(file) for file in FS.list()]
#         # file_list = "\n".join(['<li><a href="%s">%s</a></li>' %
#         #                        (url_for('serve_gridfs_file', oid=str(file._id)),
#         #                         file.name)
#         #                        for file in files])
#         # file_list = " jojo"
#         file_list = '<div>file for download</div><li><a href="%s">%s</a></li>' % (url_for('serve_gridfs_file', oid=str(file._id)),file.name)
#         #
#     else:
#         file_list=''
#     return render_template('single_post.html',conformer=conformer, file_list=file_list, default_settings=app.config,post=post['data'], meta_title=app.config['BLOG_TITLE'] + '::' + post['data']['title'])


@app.route('/q/<query>', defaults={'page': 1})
@app.route('/q/<query>/page-<int:page>')
def search_results(page, query):
    skip = (page - 1) * int(app.config['PER_PAGE'])
    if query:
        posts = postClass.get_posts(
            int(app.config['PER_PAGE']), skip, search=query)
    else:
        posts = []
        posts['data'] = []
    count = postClass.get_total_count(search=query)
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count)
    return render_template('molecule_list.html',default_settings=app.config, posts=posts['data'], pagination=pag, meta_title='Search results')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method != 'POST':
        return redirect(url_for('index'))

    query = request.form.get('query', None)
    if query:
        return redirect(url_for('search_results', query=query))
    else:
        return redirect(url_for('index'))





@app.route('/handle_application/<permalink>')
def handle_application(permalink):
    application = applicationClass.get_application_by_permalink(permalink)
    if not application['data']:
        abort(404)
    if application['data'].get('molecule_link'):
        molecule=moleculeClass.get_molecule_by_name(application['data'].get('molecule_link'))

    return render_template('handle_application.html',application=application['data'],default_settings=app.config,molecule=molecule['data'], meta_title=app.config['BLOG_TITLE'] + '::' + molecule['data']['title'])


def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


@app.route('/accept/<permalink>')
def accept(permalink):


    application=applicationClass.get_application_by_permalink(permalink)
    molecule_link=application['data'].get('molecule_link')
    molecule=moleculeClass.get_molecule_by_name(molecule_link)
    title=molecule['data'].get('title')

    archivefile = tempfile.mktemp()

    f = zipfile.ZipFile(archivefile,'w',zipfile.ZIP_DEFLATED)
    curdir=os.getcwd()
    os.chdir(moleculeClass.path)
    startdir = title
    for dirpath, dirnames, filenames in os.walk(startdir):
        for filename in filenames:
            if filename.find('~')==-1:
                f.write(os.path.join(dirpath,filename))

    os.chdir(curdir)
    f.close()
    file = open(archivefile,'r')

    msg = Message('reply for your application for %s' % application['data'].get('title'),
                  sender=("lhr", "lhrkkk@mail.ustc.edu.cn"),
                  recipients=[application['data'].get('email')]


                )
    msg.body='''
Hello dear %s,\n
Your application: \n\n%s \n\nhas passed our audit.\n
We provide the data package file for download as attachment, you should use these data under our licence which was also delivered inside the package.

----
Zijing Lin's Lab, All Rights Reserved
University of Science and Technology of China
Hefei National Laboratory for Physical Sciences at the Microscale

'''% (application['data'].get('applicant'),application['data'].get('body'))
    msg.attach(title+'.zip', "application/zip",file.read(),'attachment')

    mail.send(msg)

#     mail_config={}
#     mail_config['from_address'] = 'lhrkkk@mail.ustc.edu.cn'
#     mail_config['to_address'] = application['data'].get('email')
#     mail_config['subject'] = 'reply for your application for %s' % application['data'].get('title')
#     mail_config['content'] = '''
# Hello dear %s,\n
# Your application: \n\n%s \n\nhas passed our audit.\n
# We provide the data package file for download as attachment, you should use these data under our licence which was also delivered inside the package.
#
# ----
# Zijing Lin's Lab, All Rights Reserved
# University of Science and Technology of China
# Hefei National Laboratory for Physical Sciences at the Microscale
#
#  '''% (application['data'].get('applicant'),application['data'].get('body'))
#     filename=title+'.zip'
#     my_new_mail(mail_config['from_address'],mail_config['to_address'],mail_config['subject'],mail_config['content'],file,filename)


    application['data']['status']='Accepted'
    applicationClass.edit_application(application['data']['_id'],application['data'])
    # f.close()
    return redirect(redirect_url())


@app.route('/decline/<permalink>')
def decline(permalink):

    application=applicationClass.get_application_by_permalink(permalink)
    molecule_link=application['data'].get('molecule_link')
    molecule=moleculeClass.get_molecule_by_name(molecule_link)
    title=molecule['data'].get('title')

    msg = Message('reply for your application for %s' % application['data'].get('title'),
                  sender=("lhr", "lhrkkk@mail.ustc.edu.cn"),
                  recipients=[application['data'].get('email')]


    )
    msg.body='''
Hello dear %s,\n
Your application: \n\n%s \n\nhas not passed our audit.\n

----
Zijing Lin's Lab, All Rights Reserved
University of Science and Technology of China
Hefei National Laboratory for Physical Sciences at the Microscale

'''% (application['data'].get('applicant'),application['data'].get('body'))

    mail.send(msg)


    application['data']['status']='Declined'
    applicationClass.edit_application(application['data']['_id'],application['data'])

    return redirect(redirect_url())

@app.route('/new_application/<title>', methods=['GET', 'POST'])
def new_application(title):
    error = False
    error_type = 'validate'
    if request.method == 'POST':
        post_title = request.form.get('application-title').strip()
        post_full = request.form.get('application-full')
        email = request.form.get('email')
        applicant = request.form.get('applicant')

        attachment = None
        conformer = None

        if not post_title or not post_full:
            error = True
        else:

            post_data = {'title': post_title,
                         # 'preview': request.form.get('post-short'),
                         'body': post_full,
                         'email': email,
                         'applicant': applicant,
                         'attachment': None,
                         'conformer': None,
                         'author': post_title,
                         'molecule_link': title
            }


            post = applicationClass.validate_application_data(post_data)

            response = applicationClass.create_new_application(post)
            if response['error']:
                error = True
                error_type = 'post'
                flash(response['error'], 'error')
            else:
                flash('new application created!', 'success')
            return redirect(url_for('application_is_successful',title=title))

    else:
        if session.get('post-preview') and session['post-preview']['action'] == 'edit':
            session.pop('post-preview', None)

    # post = postClass.get_post_by_permalink(permalink)
    molecule=moleculeClass.get_molecule_by_name(title)
    if not molecule['data']:
        abort(404)

    return render_template('new_application.html',
                           default_settings=app.config,
                           meta_title='New application',
                           data_licence=app.config['DATA_LICENCE'],
                           # data_licence=default_settings['DATA_LICENCE'],
                           post = molecule['data'],
                           error=error,
                           error_type=error_type)
#
# @app.route('/new_application/<permalink>', methods=['GET', 'POST'])
# def new_application(permalink):
#     error = False
#     error_type = 'validate'
#     if request.method == 'POST':
#         post_title = request.form.get('application-title').strip()
#         post_full = request.form.get('application-full')
#         email = request.form.get('email')
#         applicant = request.form.get('applicant')
#
#         # attachment = request.files['attachment']
#         # conformer = request.files['conformer']
#         attachment = None
#         conformer = None
#
#         # print dir(request.files)
#         # print request.files.items()
#
#         if not post_title or not post_full:
#             error = True
#         else:
#             # tags = cgi.escape(request.form.get('post-tags'))
#             # tags_array = extract_tags(tags)
#             post_data = {'title': post_title,
#                          # 'preview': request.form.get('post-short'),
#                          'body': post_full,
#                          'email': email,
#                          'applicant': applicant,
#                          'attachment': None,
#                          'conformer': None,
#                          'author': post_title,
#                          'molecule_link': permalink
#
#             }
#             # 'tags': tags_array,
#
#             if attachment and allowed_file(attachment.filename):
#                 filename = secure_filename(attachment.filename)
#                 oid = FS.put(
#                     attachment, content_type=attachment.content_type, filename=filename)
#                 # print oid
#                 # print str(oid)
#                 # return redirect(url_for('serve_gridfs_file', oid=str(oid)))
#
#                 post_data['attachment'] =  oid
#
#             if conformer and allowed_file(conformer.filename):
#                 filename = secure_filename(conformer.filename)
#                 oid = FS.put(
#                     conformer, content_type=conformer.content_type, filename=filename)
#                 # print oid
#                 # print str(oid)
#                 # return redirect(url_for('serve_gridfs_file', oid=str(oid)))
#
#                 post_data['conformer'] =  oid
#
#                 # else:
#                 #     post_data = {'title': post_title,
#                 #                  # 'preview': request.form.get('post-short'),
#                 #                  'body': post_full,
#                 #                  # 'tags': tags_array,
#                 #
#                 # 'author': session['user']['username']}
#
#             post = applicationClass.validate_application_data(post_data)
#
#             response = applicationClass.create_new_application(post)
#             if response['error']:
#                 error = True
#                 error_type = 'post'
#                 flash(response['error'], 'error')
#             else:
#                 flash('new application created!', 'success')
#             return redirect(url_for('application_is_successful',permalink=permalink))
#
#     else:
#         if session.get('post-preview') and session['post-preview']['action'] == 'edit':
#             session.pop('post-preview', None)
#
#     post = postClass.get_post_by_permalink(permalink)
#     if not post['data']:
#         abort(404)
#
#     return render_template('new_application.html',
#                            default_settings=app.config,
#                            meta_title='New application',
#                            data_licence=app.config['DATA_LICENCE'],
#                            # data_licence=default_settings['DATA_LICENCE'],
#                            post = post['data'],
#                            error=error,
#                            error_type=error_type)


@app.route('/applications_list', defaults={'page': 1})
@app.route('/applications_list/page-<int:page>')
@login_required()
def manage_applications(page):
    session.pop('post-preview', None)
    skip = (page - 1) * int(app.config['PER_PAGE'])
    applications = applicationClass.get_applications(int(app.config['PER_PAGE']), skip)
    count = applicationClass.get_total_count()
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count)

    # if not applications['data']:
    #     abort(404)

    return render_template('manage_applications.html', default_settings=app.config,applications=applications['data'], pagination=pag, meta_title='applications')

@app.route('/show_applications_list', defaults={'page': 1})
@app.route('/show_applications_list/page-<int:page>')
@login_required()
def show_applications(page):
    session.pop('post-preview', None)
    skip = (page - 1) * int(app.config['PER_PAGE'])
    applications = applicationClass.get_applications(int(app.config['PER_PAGE']), skip)
    count = applicationClass.get_total_count()
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count)
    applications=applicationClass.get_view('title','email')
    applications=sorted(applications,key=lambda s:s['count'],reverse=True)
    email_applications=applicationClass.get_view('email','title')
    email_applications=sorted(email_applications,key=lambda s:s['count'],reverse=True)
    # applicationClass.get_view('email','title')
    # if not applications['data']:
    #     abort(404)

    return render_template('show_applications.html', default_settings=app.config,applications=applications, email_applications=email_applications,pagination=pag, meta_title='applications')


@app.route('/newpost', methods=['GET', 'POST'])
@login_required()
def new_post():
    error = False
    error_type = 'validate'
    if request.method == 'POST':
        post_title = request.form.get('post-title').strip()
        post_full = request.form.get('post-full')
        attachment = request.files['attachment']
        conformer = request.files['conformer']

    # print dir(request.files)
        # print request.files.items()


        if not post_title or not post_full:
            error = True
        else:
            # tags = cgi.escape(request.form.get('post-tags'))
            # tags_array = extract_tags(tags)
            post_data = {'title': post_title,
                         # 'preview': request.form.get('post-short'),
                         'body': post_full,
                         'attachment': None,
                         'conformer': None,
                         'author': session['user']['username']}
            # 'tags': tags_array,

            if attachment and allowed_file(attachment.filename):
                filename = secure_filename(attachment.filename)
                oid = FS.put(
                attachment, content_type=attachment.content_type, filename=filename)
                # print oid
                # print str(oid)
            # return redirect(url_for('serve_gridfs_file', oid=str(oid)))

                post_data['attachment'] =  oid

            if conformer and allowed_file(conformer.filename):
                filename = secure_filename(conformer.filename)
                oid = FS.put(
                    conformer, content_type=conformer.content_type, filename=filename)
                # print oid
                # print str(oid)
                # return redirect(url_for('serve_gridfs_file', oid=str(oid)))

                post_data['conformer'] =  oid

            # else:
            #     post_data = {'title': post_title,
            #                  # 'preview': request.form.get('post-short'),
            #                  'body': post_full,
            #                  # 'tags': tags_array,
            #
                             # 'author': session['user']['username']}

            post = postClass.validate_post_data(post_data)
            if request.form.get('post-preview') == '1':
                session['post-preview'] = post
                session[
                    'post-preview']['action'] = 'edit' if request.form.get('post-id') else 'add'
                if request.form.get('post-id'):
                    session[
                        'post-preview']['redirect'] = url_for('post_edit', id=request.form.get('post-id'))
                else:
                    session['post-preview']['redirect'] = url_for('new_post')
                return redirect(url_for('post_preview'))
            else:
                session.pop('post-preview', None)

                if request.form.get('post-id'):
                    response = postClass.edit_post(
                        request.form['post-id'], post)
                    if not response['error']:
                        flash('Post updated!', 'success')
                    else:
                        flash(response['error'], 'error')
                    return redirect(url_for('posts'))
                else:
                    response = postClass.create_new_post(post)
                    if response['error']:
                        error = True
                        error_type = 'post'
                        flash(response['error'], 'error')
                    else:
                        flash('New molecule created!', 'success')
    else:
        if session.get('post-preview') and session['post-preview']['action'] == 'edit':
            session.pop('post-preview', None)
    return render_template('new_post.html',
                           default_settings=app.config,
                           meta_title='New post',
                           error=error,
                           error_type=error_type)


@app.route('/post_preview')
@login_required()
def post_preview():
    post = session.get('post-preview')
    return render_template('preview.html', default_settings=app.config,post=post, meta_title='Preview post::' + post['title'])


@app.route('/posts_list', defaults={'page': 1})
@app.route('/posts_list/page-<int:page>')
@login_required()
def posts(page):
    session.pop('post-preview', None)
    skip = (page - 1) * int(app.config['PER_PAGE'])
    posts = postClass.get_posts(int(app.config['PER_PAGE']), skip)
    count = postClass.get_total_count()
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count)
    if not posts['data']:
        abort(404)

    return render_template('posts.html', default_settings=app.config,posts=posts['data'], pagination=pag, meta_title='Posts')


@app.route('/post_edit?id=<id>')
@login_required()
def post_edit(id):
    post = postClass.get_post_by_id(id)
    if post['error']:
        flash(post['error'], 'error')
        return redirect(url_for('posts'))

    if session.get('post-preview') and session['post-preview']['action'] == 'add':
        session.pop('post-preview', None)

    if not post['data']:
        abort(404)
    if post['data'].get('conformer'):
        file = FS.get(post['data']['conformer'])
        # print file
        # files = [FS.get_last_version(file) for file in FS.list()]
        # file_list = "\n".join(['<li><a href="%s">%s</a></li>' %
        #                        (url_for('serve_gridfs_file', oid=str(file._id)),
        #                         file.name)
        #                        for file in files])
        # file_list = " jojo"
        conformer = '<input type=file name=conformer value="%s" >' % (url_for('serve_gridfs_file', oid=str(file._id)))
        #
    else:
        conformer=''
    if post['data'].get('attachment'):
        file = FS.get(post['data']['attachment'])
        # print file
        # files = [FS.get_last_version(file) for file in FS.list()]
        # file_list = "\n".join(['<li><a href="%s">%s</a></li>' %
        #                        (url_for('serve_gridfs_file', oid=str(file._id)),
        #                         file.name)
        #                        for file in files])
        # file_list = " jojo"
        file_list = '<input type=file name=attachment value="%s">' % (url_for('serve_gridfs_file', oid=str(file._id)))
        file_list = '<input type=file name=attachment >'
    else:
        file_list='<input type=file name=attachment >'

    return render_template('edit_post.html',
                           meta_title='Edit post::' + post['data']['title'],
                           default_settings=app.config,
                           conformer=conformer,
                           file_list=file_list,
                           post=post['data'],
                           error=False,
                           error_type=False)



@app.route('/post_delete?id=<id>')
@login_required()
def post_del(id):
    if postClass.get_total_count() > 1:
        response = postClass.delete_post(id)
        if response['data'] is True:
            flash('Post removed!', 'success')
        else:
            flash(response['error'], 'error')
    else:
        flash('Need to be at least one post..', 'error')

    return redirect(url_for('posts'))

@app.route('/application_delete?id=<id>')
@login_required()
def application_del(id):
    if applicationClass.get_total_count() > 1:
        response = applicationClass.delete_application(id)
        if response['data'] is True:
            flash('Application removed!', 'success')
        else:
            flash(response['error'], 'error')
    else:
        flash('Need to be at least one application..', 'error')

    return redirect(redirect_url())


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = False
    error_type = 'validate'
    if request.method == 'POST':
        username = request.form.get('login-username')
        password = request.form.get('login-password')
        if not username or not password:
            error = True
        else:
            user_data = userClass.login(username.lower().strip(), password)
            if user_data['error']:
                error = True
                error_type = 'login'
                flash(user_data['error'], 'error')
            else:
                userClass.start_session(user_data['data'])
                flash('You are logged in!', 'success')
                return redirect(url_for('index'))
    else:
        if session.get('user'):
            return redirect(url_for('posts'))

    return render_template('login.html',
                           meta_title='Login',
                           default_settings=app.config,
                           error=error,
                           error_type=error_type)


@app.route('/logout')
def logout():
    if userClass.logout():
        flash('You are logged out!', 'success')
    return redirect(url_for('login'))


@app.route('/users')
@login_required()
def users_list():
    users = userClass.get_users()
    return render_template('users.html', default_settings=app.config,users=users['data'], meta_title='Users')


@app.route('/add_user')
@login_required()
def add_user():
    gravatar_url = userClass.get_gravatar_link()
    return render_template('add_user.html', default_settings=app.config,gravatar_url=gravatar_url, meta_title='Add user')


@app.route('/edit_user?id=<id>')
@login_required()
def edit_user(id):
    user = userClass.get_user(id)
    return render_template('edit_user.html', default_settings=app.config,user=user['data'], meta_title='Edit user')


@app.route('/delete_user?id=<id>')
@login_required()
def delete_user(id):
    if id != session['user']['username']:
        user = userClass.delete_user(id)
        if user['error']:
            flash(user['error'], 'error')
        else:
            flash('User deleted!', 'success')
    return redirect(url_for('users_list'))


@app.route('/save_user', methods=['POST'])
@login_required()
def save_user():
    post_data = {
        '_id': request.form.get('user-id', None).lower().strip(),
        'email': request.form.get('user-email', None),
        'old_pass': request.form.get('user-old-password', None),
        'new_pass': request.form.get('user-new-password', None),
        'new_pass_again': request.form.get('user-new-password-again', None),
        'update': request.form.get('user-update', False)
    }
    if not post_data['email'] or not post_data['_id']:
        flash('Username and Email are required..', 'error')
        if post_data['update']:
                return redirect(url_for('edit_user', id=post_data['_id']))
        else:
            return redirect(url_for('add_user'))
    else:
        user = userClass.save_user(post_data)
        if user['error']:
            flash(user['error'], 'error')
            if post_data['update']:
                return redirect(url_for('edit_user', id=post_data['_id']))
            else:
                return redirect(url_for('add_user'))
        else:
            message = 'User updated!' if post_data['update'] else 'User added!'
            flash(message, 'success')
    return redirect(url_for('edit_user', id=post_data['_id']))


@app.route('/recent_feed')
def recent_feed():
    feed = AtomFeed(app.config['BLOG_TITLE'] + '::Recent Articles',
                    feed_url=request.url, url=request.url_root)
    posts = postClass.get_posts(int(app.config['PER_PAGE']), 0)
    for post in posts['data']:
        post_entry = post['preview'] if post['preview'] else post['body']
        feed.add(post['title'], md(post_entry),
                 content_type='html',
                 author=post['author'],
                 url=make_external(
                     url_for('single_post', permalink=post['permalink'])),
                 updated=post['date'])
    return feed.get_response()


@app.route('/settings', methods=['GET', 'POST'])
@login_required()
def blog_settings():
    error = None
    error_type = 'validate'
    if request.method == 'POST':

        blog_data = {
            'title': request.form.get('blog-title', None),
            'description': request.form.get('blog-description', None),
            'data_licence': request.form.get('data-licence', None),
            'per_page': request.form.get('blog-perpage', None),
            'text_search': request.form.get('blog-text-search', None),
            'molecule_list_description':  request.form.get('molecule-list-description', None)
        }
        blog_data['text_search'] = 1 if blog_data['text_search'] else 0
        for key, value in blog_data.items():
            if not value and key != 'text_search' and key != 'description' and key != 'per_page':
                error = True
                break
        if not error:
            update_result = settingsClass.update_settings(blog_data)
            if update_result['error']:
                flash(update_result['error'], 'error')
            else:
                flash('Settings updated!', 'success')
                return redirect(url_for('blog_settings'))

    return render_template('settings.html',
                           default_settings=app.config,
                           meta_title='Settings',
                           error=error,
                           error_type=error_type)


@app.route('/install', methods=['GET', 'POST'])
def install():
    if session.get('installed', None):
        return redirect(url_for('index'))
    error = False
    error_type = 'validate'
    if request.method == 'POST':
        user_error = False
        blog_error = False

        user_data = {
            '_id': request.form.get('user-id', None).lower().strip(),
            'email': request.form.get('user-email', None),
            'new_pass': request.form.get('user-new-password', None),
            'new_pass_again': request.form.get('user-new-password-again', None),
            'update': False
        }
        blog_data = {
            'title': request.form.get('blog-title', None),
            'description': request.form.get('blog-description', None),
            'per_page': request.form.get('blog-perpage', None),
            'text_search': request.form.get('blog-text-search', None)
        }
        blog_data['text_search'] = 1 if blog_data['text_search'] else 0

        for key, value in user_data.items():
            if not value and key != 'update':
                user_error = True
                break
        for key, value in blog_data.items():
            if not value and key != 'text_search' and key != 'description':
                blog_error = True
                break
        print user_error, "haha", blog_error
        if user_error or blog_error:
            error = True
        else:
            install_result = settingsClass.install(blog_data, user_data)
            if install_result['error']:
                for i in install_result['error']:
                    if i is not None:
                        flash(i, 'error')
            else:
                session['installed'] = True
                flash('Successfully installed!', 'success')
                user_login = userClass.login(
                    user_data['_id'], user_data['new_pass'])
                if user_login['error']:
                    flash(user_login['error'], 'error')
                else:
                    userClass.start_session(user_login['data'])
                    flash('You are logged in!', 'success')
                    return redirect(url_for('posts'))
    else:
        if settingsClass.is_installed():
            return redirect(url_for('index'))

    return render_template('install.html',
                           default_settings=app.config,
                           error=error,
                           error_type=error_type,
                           meta_title='Install')


@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(400)


@app.before_request
def is_installed():
    app.config = settingsClass.get_config()
    app.jinja_env.globals['meta_description'] = app.config['BLOG_DESCRIPTION']
    app.jinja_env.globals['data_licence'] = app.config['DATA_LICENCE']
    # session['installed']=None
    if not session.get('installed', None):
        if url_for('static', filename='') not in request.path and request.path != url_for('install'):
            if not settingsClass.is_installed():
                return redirect(url_for('install'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', meta_title='404'), 404


@app.template_filter('formatdate')
def format_datetime_filter(input_value, format_="%a, %d %b %Y"):
    return input_value.strftime(format_)


settingsClass = settings.Settings(app.config)
# postClass = post.Post(app.config)
moleculeClass = molecule.Molecule(app.config)
userClass = user.User(app.config)
applicationClass = application.Application(app.config)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page
app.jinja_env.globals['csrf_token'] = generate_csrf_token
app.jinja_env.globals['meta_description'] = app.config['BLOG_DESCRIPTION']
# print app.config['BLOG_TITLE']
app.jinja_env.globals['blog_title'] = app.config['BLOG_TITLE']
# app.jinja_env.globals['recent_posts'] = postClass.get_posts(10, 0)['data']
# app.jinja_env.globals['tags'] = postClass.get_tags()['data']

if not app.config['DEBUG']:
    import logging
    from logging import FileHandler
    file_handler = FileHandler(app.config['LOG_FILE'])
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)


#################
#
# from flask_flatpages import FlatPages
# from flask_flatpages_pandoc import FlatPagesPandoc
#
#
# pages = FlatPages(app)
#
# @app.route('/test')
# def index():
#     # Articles are pages with a publication date
#     articles = (p for p in pages if 'published' in p.meta)
#     # Show the 10 most recent articles, most recent first.
#     latest = sorted(articles, reverse=True,
#                     key=lambda p: p.meta['published'])
#     return render_template('articles.html', articles=latest[:10])
#
#
#
# @app.route('/test/<path:path>/')
# def page(path):
#     page = pages.get_or_404(path)
#     template = page.meta.get('template', 'flatpage.html')
#     return render_template(template, page=page)
#

#################

from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)


if __name__ == '__main__':

    # FlatPagesPandoc("markdown", app, ["--mathjax"])
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)),
            debug=app.config['DEBUG'])
