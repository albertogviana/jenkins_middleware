from middleware.jenkins.models import Configuration as ConfigurationModel
from sqlalchemy.orm.exc import NoResultFound


def get_application_configuration(team_name):
    """
    Return a configuration object with jenkins configuration
    :param team_name: string
    :return: ConfigurationModel
    """
    try:
        return ConfigurationModel.query.filter_by(team_name=team_name).one()
    except NoResultFound:
        raise Exception('No configuration found for team %s. Please add it.' % team_name)
    except Exception as inst:
        raise Exception(str(inst))

