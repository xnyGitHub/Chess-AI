"""Module that connects the MVC together"""
import event_manager
import model
import view
import controller


def run():
    """Main Entry point"""
    ev_manager = event_manager.EventManager()
    gamemodel = model.GameEngine(ev_manager)
    controller.KeyboardAndMouse(ev_manager, gamemodel)
    view.PygameView(ev_manager, gamemodel)
    gamemodel.run()


if __name__ == "__main__":
    run()
