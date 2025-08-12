# logger.py
import logging
import colorlog

class QALogger(logging.Logger):
    """
    A custom logger that adds 'QUESTION' and 'ANSWER' logging levels.
    """
    QUESTION_LEVEL = 25
    ANSWER_LEVEL = 26

    # Add the custom levels to the logging system
    logging.addLevelName(QUESTION_LEVEL, "QUESTION")
    logging.addLevelName(ANSWER_LEVEL, "ANSWER")

    def question(self, msg, *args, **kwargs):
        """
        Logs a message with the 'QUESTION' level.
        """
        if self.isEnabledFor(self.QUESTION_LEVEL):
            self._log(self.QUESTION_LEVEL, msg, args, **kwargs)

    def answer(self, msg, *args, **kwargs):
        """
        Logs a message with the 'ANSWER' level.
        """
        if self.isEnabledFor(self.ANSWER_LEVEL):
            self._log(self.ANSWER_LEVEL, msg, args, **kwargs)

# Set the custom logger class to be used by the logging module
logging.setLoggerClass(QALogger)