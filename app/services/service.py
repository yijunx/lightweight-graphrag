from app.repositories.base_graph import BaseFriendRepo


class FriendService:
    """SERIVCE DOES NOT KNOW NEO4J or WEAVIATE!!!!"""
    def __init__(self, friend_repo: BaseFriendRepo) -> None:
        self.friend_repo = friend_repo

    def something_needs_add_friend(self):
        # some other business logic

        # start to talking to graph db only when required!!!
        # so that, the time duration of this connection is minimized
        with self.friend_repo.get_driver() as driver:
            self.friend_repo.add_friend(driver=driver, name="tom", friend_name="emily")

    def something_needs_print_friends(self):
        # some other business logic

        # start to talking to graph db only when required!!!
        # so that, the time duration of this connection is minimized
        with self.friend_repo.get_driver() as driver:
            self.friend_repo.print_friends(driver=driver, name="tom")
