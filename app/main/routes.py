from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, \
    current_app, abort
from flask_login import current_user, login_required
import os
import yaml
import re
from app import photos
from app.models import User
from app.main import bp
from app.main.forms import EditToolForm, DeleteToolForm, DeleteToolButton

admins = ['cfede']

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    yamls_to_read = get_file_names()
    yamls = load_yamls(yamls_to_read)

    if current_user.username not in admins:
        yamls = find_pages_owned(current_user.username, yamls)

    toolnames = [yaml['toolname-trim'] for yaml in yamls]

    return render_template('index.html',
                            toolnames=toolnames,
                            title=('Home'))


@bp.route("/tool/<toolname>", methods=['GET', 'POST'])
@login_required
def edit_tool(toolname):
    try:
        tool_yaml = load_yaml(toolname+".yml")
    except:
        tool_yaml = {}
        tool_yaml['owners']=[]

    form = EditToolForm()
    #delete_button =DeleteToolButton()


    if form.validate_on_submit():
        tool_yaml["toolname"] = form.toolname.data
        tool_yaml["toolname-trim"] = form.trim_toolname(form.toolname.data)
        tool_yaml["category"] = form.category.data
        tool_yaml["owners"] = [form.owner1.data, form.owner2.data, form.owner3.data]
        tool_yaml["about"] = form.about.data

        if form.photo.data:
            try:
                os.remove("page_data/screenshots/"+form.trim_toolname(form.toolname.data)+".jpg")
            except:
                pass
            photos.save(form.photo.data,
                        name=form.trim_toolname(form.toolname.data)+".jpg")
        else:
            if not os.path.exists("page_data/screenshots/"+form.trim_toolname(form.toolname.data)+".jpg"):
                flash("There isn't a screenshot on file. Please upload one.")
                return(redirect(url_for('main.edit_tool', toolname=toolname)))

        save_yaml(tool_yaml, tool_yaml['toolname-trim'])

        flash('Your changes have been saved')
        return(redirect(url_for('main.index')))
    elif request.method == "GET":
        try:
            form.toolname.data=tool_yaml["toolname"]
            form.category.data=tool_yaml["category"]
            form.owner1.data=tool_yaml["owners"][0]
            form.owner2.data=tool_yaml["owners"][1]
            form.owner3.data=tool_yaml["owners"][2]
            form.about.data=tool_yaml["about"]
        except KeyError:
            pass
    return render_template('edit_tool.html', title="Edit Tool",
                            toolname=toolname, form=form)
                            #delete_button=delete_button)

@bp.route("/tool/<toolname>/delete", methods=['GET', "POST"])
@login_required
def delete_tool(toolname):
    form = DeleteToolForm()
    try:
        tool_yaml = load_yaml(toolname+".yml")
        if form.validate_on_submit():
            if current_user.username in tool_yaml['owners'] or \
               current_user.username in admins:
                if toolname == form.toolname.data:
                    remove_yaml(toolname)
                    os.remove("page_data/screenshots/"+toolname+".jpg")
                    flash(toolname + ' has been deleted')
                    return(redirect(url_for('main.index')))
                else:
                    flash("The name you entered did not match")
            else:
                flash("You are not an admin or an owner")
    except:
        abort(404)
    return(render_template("delete_tool.html",
                            title="Delete Tool",
                            toolname = toolname,
                            form=form))


def get_file_names(page_dir="page_data"):
    file_names = os.listdir(page_dir)
    return [file_name for file_name in file_names \
            if re.match(r'.*\.yml', file_name)]

def load_yaml(file_name, page_dir="page_data"):
    file_name = page_dir + "/" + file_name
    with open(file_name) as f:
         return(yaml.load(f, Loader=yaml.FullLoader))

def load_yamls(file_names, page_dir="page_data"):
    return([load_yaml(file_name, page_dir) for file_name in file_names])

def save_yaml(a_dict, filename, page_dir="page_data"):
    with open(page_dir+"/"+filename+".yml", 'w') as file:
        yaml.dump(a_dict, file)

def remove_yaml(toolname, page_dir="page_data"):
    os.remove(page_dir+"/"+toolname+".yml")


def find_pages_owned(username, yamls):
    def match_username(username, yaml):
        if username in yaml['owners']:
            return yaml
    out = [match_username(username, yaml) for yaml in yamls]
    out = [yaml for yaml in out if yaml is not None]
    return out
