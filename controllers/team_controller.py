from flask import Flask, render_template, request, redirect, url_for
from flask import Blueprint
from models.team import Team
import repositories.team_repository as team_repository
import repositories.match_repository as match_repository
import repositories.match_result_repository as match_result_repository


teams_blueprint = Blueprint("teams", __name__)

@teams_blueprint.route("/teams")
def teams():
    teams = team_repository.select_all() 
    return render_template("teams/index.jinja", teams = teams)

@teams_blueprint.route("/teams/<id>")
def show(id):
    team = team_repository.select(id)
    fixture_matches = match_repository.select_pending_for_team(team)
    # match = match_result_repository.select(id)
    # match_result = match_result_repository.select_pending()
    return render_template("teams/show.jinja", team=team, fixture_matches=fixture_matches)

@teams_blueprint.route('/teams', methods=['POST']) 
def add_teams():
    name=request.form['team_name']
    new_team=Team(name)
    team_repository.save(new_team)
    return redirect('/teams')
    
@teams_blueprint.route('/teams/<id>/delete', methods=['POST'])
def delete_team(id):
   team_repository.delete(id)
   return redirect('/teams')

# route to get the edit form
#  /teams/<id>/edit - GET
# get a hold of the team by the id
# present a form - the form should have the name already in the text input

@teams_blueprint.route('/teams/<id>/edit', methods=['Get'])
def edit_team(id):
    team = team_repository.select(id)
    return render_template('teams/edit.jinja', team = team)


@teams_blueprint.route("/teams/<id>/edit", methods=['POST'])
def update_team(id):
    # get the name from the form
    team_name = request.form['team_name_updated']
    team_update = Team(team_name, id)
    team_repository.update(team_update)
    return redirect(url_for('teams.edit_team', id = id) )

