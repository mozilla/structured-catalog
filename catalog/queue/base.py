from abc import (
    ABCMeta,
    abstractmethod,
)

class BaseQueue(object):

    @abstractmethod
    def push(self, job):
        """
        Push a job onto the queue

        :param job: a job object to push onto the queue
        """

    @abstractmethod
    def get(self):
        """
        Retrieve the next unprocessed job. Some implementations may also remove
        the job from the queue.

        :returns: a job object
        """

    @abstractmethod
    def remove(self, job):
        """
        Remove the specified job from the queue.

        :param job: a job object to remove from the queue
        """
