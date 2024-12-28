-- +migrate Up
create table users
(
    id            serial primary key,
    username      varchar(64) unique  not null,
    email         varchar(254) unique not null,
    password_hash varchar(128)        not null
);

create table posts
(
    id         serial primary key,
    content    varchar(2048) not null,
    user_id    integer       not null,
    created_at timestamp,
    updated_at timestamp,
    constraint fk_user_id foreign key (user_id)
        references users (id) on delete cascade
);

create table comments
(
    id                serial primary key,
    content           varchar(512) not null,
    created_at        timestamp,
    updated_at        timestamp,
    user_id           integer      not null,
    post_id           integer      not null,
    parent_comment_id integer,
    constraint fk_user_id foreign key (user_id)
        references users (id) on delete cascade,
    constraint fk_post_id foreign key (user_id)
        references posts (id) on delete cascade,
    constraint fk_comment_id foreign key (user_id)
        references comments (id) on delete cascade

);

-- +migrate Down
drop table users;
drop table posts;
drop table comments;
