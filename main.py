from fake_data_generate import (
    generate_fake_user,
    generate_fake_comments,
    generate_fake_dest,
    generate_fake_iternaries,
    generate_fake_votes
)


if __name__ == "__main__":

    generate_fake_user(10)
    generate_fake_dest(20)
    generate_fake_iternaries(10)
    generate_fake_comments(20)
    generate_fake_votes(10)
