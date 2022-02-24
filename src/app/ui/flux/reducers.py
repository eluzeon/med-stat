from src.app.ui.flux import actions
from src.app.ui.flux.actions import Action
from src.app.ui.state import AppState


def file_reducer(state: AppState, action: Action):
    if isinstance(action, actions.SelectFileAction):
        state.file_path = action.payload.path
        return
