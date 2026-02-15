-- Minimal schema for AutoAppDev controller state.

create table if not exists app_config (
  key text primary key,
  value jsonb not null,
  updated_at timestamptz not null default now()
);

create table if not exists chat_messages (
  id bigserial primary key,
  role text not null,
  content text not null,
  created_at timestamptz not null default now()
);

create table if not exists inbox_messages (
  id bigserial primary key,
  role text not null,
  content text not null,
  created_at timestamptz not null default now()
);

create table if not exists outbox_messages (
  id bigserial primary key,
  role text not null,
  content text not null,
  created_at timestamptz not null default now()
);

create index if not exists outbox_messages_created_at_idx on outbox_messages(created_at);

create table if not exists pipeline_runs (
  id bigserial primary key,
  status text not null,
  pid integer,
  started_at timestamptz not null default now(),
  stopped_at timestamptz,
  script text not null,
  cwd text not null,
  args jsonb not null default '[]'::jsonb
);

create table if not exists pipeline_state (
  id integer primary key,
  state text not null,
  pid integer,
  run_id bigint,
  started_at timestamptz,
  paused_at timestamptz,
  resumed_at timestamptz,
  stopped_at timestamptz,
  updated_at timestamptz not null default now()
);

insert into pipeline_state(id, state) values (1, 'stopped') on conflict (id) do nothing;

create table if not exists pipeline_scripts (
  id bigserial primary key,
  title text not null default '',
  script_text text not null,
  script_version integer not null default 1,
  script_format text not null default 'aaps',
  ir jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists pipeline_scripts_updated_at_idx on pipeline_scripts(updated_at);

create table if not exists action_definitions (
  id bigserial primary key,
  title text not null,
  kind text not null,
  spec jsonb not null,
  enabled boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists action_definitions_updated_at_idx on action_definitions(updated_at);

create table if not exists workspace_configs (
  workspace text primary key,
  config jsonb not null,
  updated_at timestamptz not null default now()
);

create index if not exists workspace_configs_updated_at_idx on workspace_configs(updated_at);
