import os
import re

from settings import BASE_FOLDER, TRANSLATOR, TRANSLATOR_URL, LANG
import importlib

module = importlib.import_module(f'translations_{LANG}')
translation_dict = getattr(module, 'translation_dict')

script_path = os.path.dirname(os.path.abspath(__file__))

BASE_PATH = f'{BASE_FOLDER}zed-src/'
os.chdir(BASE_PATH)

TRANSLATOR_LABEL = translation_dict['translator']

# 用 {{}} 来标记要翻译的内容
# use {{}} to mark the content you want to translate

# pat = re.compile('{{(.*?)}}', flags=re.DOTALL + re.MULTILINE)
# pat = re.compile(r'\{\{([^{}]+)\}\}', flags=re.DOTALL + re.MULTILINE)
pat = re.compile('{{(.*)}}', flags=re.DOTALL + re.MULTILINE)

# check which file is not in use anymore
missing_files = []
# check which translation is not in use anymore
used_translations = [
    'translator',
]
unused_translations = []
missing_translations = []


def translate(m):
    s = m.group(1)
    trans = translation_dict.get(s, None)
    if not trans:
        trans = s
        missing_translations.append(s)
    else:
        used_translations.append(s)

    return trans


def replace_in_file(file_path, translation, base_path=BASE_PATH):
    file_full_path = os.path.join(base_path, file_path)
    if not os.path.exists(file_full_path):
        missing_files.append(file_path)
        return

    with open(file_full_path, 'r') as f:
        content = f.read()

    for ori_mark in translation:
        ori_content = ori_mark.replace('{{', '').replace('}}', '')

        trans = pat.sub(translate, ori_mark)

        content = content.replace(ori_content, trans)

    with open(file_full_path, 'w') as f:
        f.write(content)


# 关于页面添加翻译者信息
# add translator info in about page :)
about_file_path = f'crates/zed/src/zed.rs'
with open(about_file_path, 'r') as f:
    content = f.read()
    if TRANSLATOR_LABEL not in content:
        content = content.replace(
            '"{release_channel} {version}"',
            '"{release_channel} {version} '
            + f'\\n {TRANSLATOR_LABEL} {TRANSLATOR} \\n {TRANSLATOR_URL}'
            + ' "',
        )
with open(about_file_path, 'w') as f:
    f.write(content)

# fix prompt font family issue
about_file_path = f'crates/zed/src/zed/linux_prompts.rs'
with open(about_file_path, 'r') as f:
    content = f.read()
    if TRANSLATOR_LABEL not in content:
        content = content.replace('.font_family("Zed Sans")', '.font_family("Noto Sans")')
with open(about_file_path, 'w') as f:
    f.write(content)


# 下面一堆是正则匹配规则, 读代码的时候下面这一段可以跳过, 直接看最后面几行
# TL;DR, the following codes are regex matches, you can jump to the last few lines.

# ================================= regex begin ================================

file_path = 'crates/activity_indicator/src/activity_indicator.rs'
translation = [
    'message: "{{Checking for Zed updates…}}"',
    'message: "{{Downloading Zed update…}}"',
    'message: "{{Installing Zed update…}}"',
    'message: "{{Click to restart and update Zed}}"',
    'message: "{{Auto update failed}}"',
    'format!("{{Downloading {}...}}"',
    'format!("{{Formatting failed: {}. Click to see logs.}}"',
    'format!("{{Updating {extension_id} extension…}}"',
    'format!(\n                    "{{Checking for updates to {}...}}"',
    'format!(\n                    "{{Failed to download {}. Click to show error.}}"',
    '"{{Checking for Zed updates…}}".to_string()',
    '"{{Downloading Zed update…}}".to_string()',
    '"{{Installing Zed update…}}".to_string()',
    '"{{Click to restart and update Zed}}".to_string()',
    '"{{Auto update failed}}".to_string()',
    'format!("{{Language server error:}}',
]
replace_in_file(file_path, translation)

file_path = 'crates/anthropic/src/anthropic.rs'
translation = [
    '"{{Ping}}".to_string()',
    '"{{Respond to ping with pong}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/assistant/src/assistant.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/assistant/src/assistant_panel.rs'
translation = [
    'Tooltip::text("{{Prompt Library…}}"',
    'action("{{Quote Selection}}"',
    'format!("{{Edits from {}}}"',
    'format!("{{error: {error}}}"',
    'format!("{{Indexing {crate_name}…}}"',
    'Label::new("{{Send}}")',
    'Label::new("{{You}}")',
    'Label::new("{{Assistant}}")',
    'Label::new("{{System}}")',
    'Some("{{Assistant Panel}}")',
    '    "{{AssistantPanel}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/assistant/src/completion_provider/anthropic.rs'
translation = [
    'Label::new("{{Click on}}")',
    'Label::new("{{in the status bar to close this panel.}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/assistant/src/completion_provider/cloud.rs'
translation = [
    'Button::new("sign_in", "{{Sign in}}")',
    'Label::new("{{Sign in to enable collaboration.}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/assistant/src/completion_provider/ollama.rs'
translation = [
    'Label::new("{{Get Ollama}}")',
    'Label::new("{{Retry}}")',
    'Label::new("{{Once Ollama is on your machine, make sure to download a model or two.}}")',
    'Label::new("{{View Available Models}}")',
    'Label::new("{{To use Ollama models via the assistant, Ollama must be running on your machine with at least one model downloaded.}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/assistant/src/completion_provider/open_ai.rs'
translation = [
    'Label::new("{{Click on}}")',
    'Label::new("{{in the status bar to close this panel.}}")',
    '"{{credentials not found}}"',
    '"{{missing api key}}"',
    '"{{To use the assistant panel or inline assistant, you need to add your OpenAI API key.}}",',
    '" - {{You can create an API key at: platform.openai.com/api-keys}}",',
    '" - {{Make sure your OpenAI account has credits}}",',
    "{{Having a subscription for another service like GitHub Copilot won't work.}}",
    '{{Paste your OpenAI API key below and hit enter to use the assistant:}}',
    '"{{You can also assign the OPENAI_API_KEY environment variable and restart Zed.}}",',
]
replace_in_file(file_path, translation)

file_path = 'crates/assistant/src/inline_assistant.rs'
translation = [
    'Tooltip::text("{{Cancel Assist}}"',
    'action("{{Cancel Assist}}"',
    'action("{{Transform}}"',
    'action("{{Confirm Assist}}"',
    'action(\n                                            "{{Toggle Assistant Panel}}"',
    'format!("{{Inline assistant error: {}}}"',
    'format!(\n                                                "{{{} Additional Context Tokens from Assistant}}"',
    'set_placeholder_text("{{Add a prompt…}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/assistant/src/model_selector.rs'
translation = [
    'action("{{Change Model}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/assistant/src/prompt_library.rs'
translation = [
    'Tooltip::text("{{Remove from Default Prompt}}"',
    'Tooltip::text("{{Delete Prompt}}"',
    'action("{{New Prompt}}"',
    'action(\n                                                    "{{Delete Prompt}}"',
    'format!(\n                    "{{Are you sure you want to delete {}}}"',
    'format!(\n                                                            "{{Model: {}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/assistant/src/slash_command/diagnostics_command.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/assistant/src/slash_command/fetch_command.rs'
translation = [
    'format!("{{fetch {}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/assistant/src/slash_command/file_command.rs'
translation = [
    '"{{untitled}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/assistant/src/slash_command/now_command.rs'
translation = [
    'format!("{{Today is {now}.}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/assistant/src/slash_command/prompt_command.rs'
translation = [
    'format!("{{no prompt found with title {:?}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/assistant/src/slash_command/rustdoc_command.rs'
translation = [
    'format!(\n                        "{{rustdoc ({source}): {crate_path}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/assistant/src/slash_command/search_command.rs'
translation = [
    'format!("{{Search results for {query}:}}',
]
replace_in_file(file_path, translation)

file_path = 'crates/assistant_tooling/src/project_context.rs'
translation = [
    '"{{project structure:}}',
]
replace_in_file(file_path, translation)

file_path = 'crates/assistant_tooling/src/tool_registry.rs'
translation = [
    'description: "{{Fetches the current weather for a given location.}}"',
    'format!("{{No such tool: {}}}"',
    'format!("{{temperature: {}}}"',
    '"{{None}}".to_string()',
    '"{{get_current_weather}}".to_string()',
    '"{{Fetches the current weather for a given location.}}".to_string()',
    '"{{San Francisco}}".to_string()',
    '"{{Celsius}}".to_string()',
    'Label::new("{{No such tool}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/audio/src/assets.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/auto_update/src/auto_update.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/auto_update/src/update_notification.rs'
translation = [
    'format!(\n                        "{{Updated to {app_name} {}}}"',
    'Label::new("{{View the release notes}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/breadcrumbs/src/breadcrumbs.rs'
translation = [
    '"{{Show symbol outline}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/channel/src/channel_store.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/channel/src/channel_store_tests.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/cli/src/main.rs'
translation = [
    'format!("{{Args bundle path {bundle_path:?} canonicalization}}"',
    'format!("{{Reading *.app bundle plist file at {plist_path:?}}}"',
    'format!("{{Bundle path {bundle_path:?} has no parent}}"',
    'format!("{{Reading dev bundle plist file at {plist_path:?}}}"',
    'format!("{{invalid app path {app_path:?}}}"',
    'format!("{{Executable {executable:?} path has no parent}}"',
    'format!("{{Log file creation in {executable_parent:?}}}"',
    'format!("{{Cloning descriptor for file {subprocess_stdout_file:?}}}"',
    'format!("{{Spawning {command:?}}}"',
    'format!("{{id of app}}',
]
replace_in_file(file_path, translation)

file_path = 'crates/client/src/client.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/client/src/telemetry.rs'
translation = [
    'format!("{{open {} project}}"',
    '"{{unknown}}".to_string()',
    '"{{close}}".to_string()',
    '"{{test}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/api.rs'
translation = [
    'format!("{{user {impersonate} does not exist}}"',
    '"{{missing authorization header}}".to_string()',
    '"{{invalid authorization header}}".to_string()',
    '"{{invalid authorization token}}".to_string()',
    '"{{you do not have permission to impersonate other users}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/api/events.rs'
translation = [
    '"{{Possible hang detected on main thread:}}".to_string()',
    '"{{<unknown>}}".to_string()',
    '"{{Panic request}}".to_string()',
    'format!("{{failed to upload to table}}',
    '{{*Version:*}}',
    '{{*OS:*}}',
    '{{*Incident:*}}',
    '{{and {} more}}",',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/api/extensions.rs'
translation = [
    'format!("{{failed to download manifest for extension {extension_id} version {version}}}"',
    'format!("{{invalid version for extension {extension_id} version {version}}}"',
    'format!(\n                "{{invalid manifest for extension {extension_id} version {version}: {}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/api/ips_file.rs'
translation = [
    'format!("{{Panic `{}`}}"',
    'format!("{{Exception `{}`}}"',
    'format!("{{Crash `{}`}}"',
    'format!("{{  and {} more...}}"',
    'format!(\n                    "{{ on thread {} ({})}}"',
    'format!(\n                    "{{ on thread {} ({})}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/auth.rs'
translation = [
    '"{{missing authorization header}}".to_string()',
    '"{{missing dev-server-token token in authorization header}}".to_string()',
    '"{{missing user id in authorization header}}".to_string()',
    '"{{missing access token in authorization header}}".to_string()',
    '"{{invalid credentials}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/db/queries/channels.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/db/tables/channel.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/db/tests.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/db/tests/buffer_tests.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/db/tests/contributor_tests.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/db/tests/db_tests.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/db/tests/extension_tests.rs'
translation = [
    'description: "{{an extension}}"',
    'description: "{{a good extension}}"',
    'description: "{{a great extension}}"',
    'description: "{{a real good extension}}"',
    'description: "{{an old extension}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/db/tests/feature_flag_tests.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/lib.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/main.rs'
translation = [
    '"{{ok}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/rpc.rs'
translation = [
    '"{{another dev server connected with the same token}}".to_string()',
    '"{{client must be upgraded}}".to_string()',
    '"{{no version header found}}".to_string()',
    '"{{Cannot create a remote project when the dev server is offline}}".to_string()',
    '"{{Dev server name cannot be empty}}".to_string()',
    '"{{dev server token was regenerated}}".to_string()',
    '"{{dev server was deleted}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/seed.rs'
translation = [
    'format!("{{failed to load {}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/tests.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/tests/channel_message_tests.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/tests/channel_tests.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/tests/dev_server_tests.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/tests/editor_tests.rs'
translation = [
    'title: "{{Inline into all callers}}"',
    'format!("{{message for idx-{}}}"',
    '"{{Inline into all callers}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/tests/following_tests.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/tests/integration_tests.rs'
translation = [
    '"{{Test hover content.}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/tests/notification_tests.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/tests/random_channel_buffer_tests.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/tests/random_project_collaboration_tests.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/tests/randomized_test_helpers.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/collab/src/tests/test_server.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/collab_ui/src/channel_view.rs'
translation = [
    'format!("{{#{} (read-only)}}"',
    'format!("{{#{} (disconnected)}}"',
    'menu.entry("{{Copy link to section}}"',
    '"{{channel notes (disconnected)}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab_ui/src/chat_panel.rs'
translation = [
    'Tooltip::text("{{Go to message}}"',
    'Tooltip::text("{{Reply}}"',
    'Tooltip::text("{{Edit}}"',
    'Tooltip::text("{{More}}"',
    'Tooltip::text("{{Cancel edit message}}"',
    'Tooltip::text("{{Close reply}}"',
    'menu.entry(\n                    "{{Copy message text}}"',
    'menu.entry(\n                        "{{Delete message}}"',
    '"{{Chat}}".to_string()',
    '"{{Here is a link https://zed.dev to zeds website}}".to_string()',
    '"{{**Here is a link https://zed.dev to zeds website**}}".to_string()',
    'Button::new("toggle-collab", "{{Open}}")',
    'Label::new("{{Message has been deleted...}}")',
    'Label::new("{{Select a channel to chat in.}}")',
    'Label::new("{{Replying to }}")',
    '"{{Chat Panel}}"',
    '"{{ChatPanel}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab_ui/src/chat_panel/message_editor.rs'
translation = [
    'format!("{{Message #{channel_name}}}"',
    'set_placeholder_text("{{Message Channel}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab_ui/src/collab_panel.rs'
translation = [
    'Tooltip::text("{{Leave Call}}"',
    'Tooltip::text("{{Open shared screen}}"',
    'Tooltip::text("{{Open Channel Notes}}"',
    'Tooltip::text("{{Open Chat}}"',
    'Tooltip::text("{{Open Project}}"',
    'Tooltip::text("{{Copy channel link}}"',
    'Tooltip::text("{{Search for new contact}}"',
    'Tooltip::text("{{Create a channel}}"',
    'Tooltip::text("{{Decline invite}}"',
    'Tooltip::text("{{Accept invite}}"',
    'Tooltip::text("{{Cancel invite}}"',
    'Tooltip::text("{{Open channel chat}}"',
    'Tooltip::text("{{Open channel notes}}"',
    'format!("{{Follow {}}}"',
    'format!("{{Open {}}}"',
    '''format!("{{Move '#{}' here}}"''',
    'format!("{{Invite {} to join}}"',
    'format!("{{Call {}}}"',
    'format!("{{ {} is offline}}"',
    'format!("{{ {} is on a call}}"',
    'format!("{{Invite {} to join call}}"',
    'menu.entry("{{Remove Contact}}"',
    'menu.entry(\n                    "{{Grant Mic Access}}"',
    'menu.entry(\n                    "{{Grant Write Access}}"',
    'menu.entry(\n                        "{{Move this channel}}"',
    'menu.entry(\n                    "{{Delete}}"',
    'menu.entry(\n                    "{{Leave Channel}}"',
    '"{{untitled}}".to_string()',
    '"{{To make a channel public, its parent channel must be public.}}".to_string()',
    '"{{To make a channel private, all of its subchannels must be private.}}".to_string()',
    'Button::new("sign_in", "{{Sign in}}")',
    'Label::new("{{Calling}}")',
    'Label::new("{{Guest}}")',
    'Label::new("{{Mic only}}")',
    'Label::new("{{Screen}}")',
    'Label::new("{{notes}}")',
    'Label::new("{{chat}}")',
    'Label::new("{{Sign in to enable collaboration.}}")',
    'Label::new("{{Add a Contact}}")',
    'Label::new("{{Join channel}}")',
    '''{{Move '#{}' here}}''',
    '"{{New Subchannel}}"',
    '"{{Rename}}",',
    '"{{Manage Members}}",',
    '"{{Make Channel Private}}",',
    '"{{Make Channel Public}}",',
    'format!("{{Are you sure you want to leave}}',
    '["{{Leave}}",',
    ' "{{Cancel}}"],',
    '"{{Are you sure you want to remove the channel}}',
    '["{{Remove}}",',
    '"{{Are you sure you want to remove \\"{}\\" from your contacts?"}}',
    '"{{Collab Panel}}"',
    # maybe a typo here
    '"{{CollabPanel}}"',
    '"{{Work with your team in realtime with collaborative editing, voice, shared notes and more.}}";',
    '"{{Expand Subchannels}}"',
    '"{{Collapse Subchannels}}"',
    '"{{Open Notes}}",',
    '"{{Open Chat}}",',
    '"{{Copy Channel Link}}",',
    '"{{Failed to join project}}",',
    '"{{Failed to create channel}}",',
    '"{{Failed to hang up}}"',
    '"{{Failed to set channel visibility}}"',
    '"{{Failed to move channel}}"',
    'SharedString::from("{{Requests}}"),',
    'SharedString::from("{{Contacts}}"),',
    'SharedString::from("{{Channels}}"),',
    'SharedString::from("{{Invites}}"),',
    'SharedString::from("{{Online}}"),',
    'SharedString::from("{{Offline}}"),',
    'set_placeholder_text("{{Filter...}}",',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab_ui/src/collab_panel/channel_modal.rs'
translation = [
    'menu.entry("{{Demote to Guest}}"',
    'menu.entry("{{Promote to Admin}}"',
    'menu.entry("{{Remove from Channel}}"',
    'Button::new("copy-link", "{{Copy Link}}")',
    'Label::new("{{Public}}")',
    'Label::new("{{Manage Members}}")',
    'Label::new("{{Invite Members}}")',
    'Label::new("{{Invited}}")',
    'Label::new("{{Admin}}")',
    'Label::new("{{Guest}}")',
    'Label::new("{{You}}")',
    'Label::new("{{Member}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab_ui/src/collab_panel/contact_finder.rs'
translation = [
    'Label::new("{{Contacts}}")',
    'Label::new("{{Invite new contacts}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab_ui/src/collab_titlebar_item.rs'
translation = [
    'Tooltip::text("{{Leave call}}"',
    'Tooltip::text("{{Cannot share microphone}}"',
    'Tooltip::text("{{Deafen Audio}}"',
    'Tooltip::text("{{Open Application Menu}}"',
    'Tooltip::text("{{Project is hosted on a dev server}}"',
    'Tooltip::text("{{Disconnected}}"',
    'Tooltip::text("{{Toggle User Menu}}"',
    'action("{{Open Command Palette}}"',
    'action("{{Open a new Project...}}"',
    'action("{{About Zed}}"',
    'action("{{Welcome}}"',
    'action("{{Give Feedback}}"',
    'action("{{Check for Updates}}"',
    'action("{{View Telemetry}}"',
    'action("{{Quit}}"',
    'action("{{Settings}}"',
    'action("{{Key Bindings}}"',
    'action("{{Themes…}}"',
    'action("{{Extensions}}"',
    'action("{{Sign Out}}"',
    'action(\n                                "{{Add Folder to Project...}}"',
    'action(\n                                "{{Open Recent Projects...}}"',
    'action(\n                                "{{View Dependency Licenses}}"',
    'action(\n                    "{{Recent Projects}}"',
    'format!("{{Follow {login}}}"',
    'format!("{{{} is muted}}"',
    'format!(\n                            "{{{} is sharing this project. Click to follow.}}"',
    '"{{Open recent project}}".to_string()',
    'Button::new("disconnected", "{{Disconnected}}")',
    'Button::new("sign_in", "{{Sign in}}")',
    'Label::new("{{Buffer Font Size}}")',
    'Label::new("{{UI Font Size}}")',
    'menu.header("{{Workspace}}")',
    '.header("{{Project}}")',
    '.header("{{Help}}")',
    '"{{Documentation}}",',
    '"{{Recent Projects}}",',
    '"{{Recent Branches}}",',
    '"{{Local branches only}}",',
    '"{{Please restart Zed to Collaborate}}",',
    '"{{Updating...}}",',
    '"{{Please update Zed to Collaborate}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab_ui/src/collab_ui.rs'
translation = [
    '{{Please check that you have given Zed permissions to record your screen in Settings.}}",',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab_ui/src/notification_panel.rs'
translation = [
    'format!("{{{} wants to add you as a contact}}"',
    'format!("{{{} accepted your contact invite}}"',
    'format!(\n                        "{{{} invited you to join the #{channel_name} channel}}"',
    'Button::new("decline", "{{Decline}}")',
    'Button::new("accept", "{{Accept}}")',
    'Button::new("sign_in_prompt_button", "{{Sign in}}")',
    'Label::new("{{Notifications}}")',
    'Label::new("{{Sign in to view notifications.}}")',
    'Label::new("{{You have no notifications.}}")',
    ' {{mentioned you in}} ',
    # maybe a typo here
    '"{{NotificationPanel}}"',
    '"{{Notification Panel}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab_ui/src/notifications/incoming_call_notification.rs'
translation = [
    'format!(\n                "{{{} is sharing a project in Zed}}"',
    'Button::new("accept", "{{Accept}}")',
    'Button::new("decline", "{{Decline}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab_ui/src/notifications/project_shared_notification.rs'
translation = [
    'format!(\n                "{{is sharing a project in Zed{}}}"',
    'Button::new("open", "{{Open}}")',
    'Button::new("dismiss", "{{Dismiss}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/collab_ui/src/notifications/stories/collab_notification.rs'
translation = [
    'Button::new("accept", "{{Accept}}")',
    'Button::new("decline", "{{Decline}}")',
    'Button::new("open", "{{Open}}")',
    'Button::new("dismiss", "{{Dismiss}}")',
    'Label::new("{{maxdeviant is sharing a project in Zed}}")',
    'Label::new("{{iamnbutler}}")',
    'Label::new("{{is sharing a project in Zed:}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/copilot/src/copilot.rs'
translation = [
    '"{{plaintext}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/copilot/src/copilot_completion_provider.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/copilot/src/sign_in.rs'
translation = [
    'Button::new("copilot-enable-cancel-button", "{{Cancel}}")',
    'Button::new("copilot-enabled-done-button", "{{Done}}")',
    'Button::new("copilot-subscribe-button", "{{Subscribe on GitHub}}")',
    'Button::new("copilot-subscribe-cancel-button", "{{Cancel}}")',
    'Label::new("{{Using Copilot requires an active subscription on GitHub.}}")',
    'Label::new("{{Paste this code into GitHub after clicking the button below.}}")',
    'Label::new("{{You can enable Copilot in your settings.}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/db/src/db.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/db/src/kvp.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/db/src/query.rs'
translation = [
    'format!(\n                "{{Error in {}, exec failed to execute or parse for: {}}}"',
    'format!(\n                    "{{Error in {}, exec failed to execute or parse for: {}}}"',
    'format!(\n                    "{{Error in {}, exec_bound failed to execute or parse for: {}}}"',
    'format!(\n                        "{{Error in {}, exec_bound failed to execute or parse for: {}}}"',
    'format!(\n                        "{{Error in {}, exec_bound failed to execute or parse for: {}}}"',
    'format!(\n                    "{{Error in {}, select_row failed to execute or parse for: {}}}"',
    'format!(\n                        "{{Error in {}, select_row failed to execute or parse for: {}}}"',
    'format!(\n                    "{{Error in {}, exec_bound failed to execute or parse for: {}}}"',
    'format!(\n                        "{{Error in {}, exec_bound failed to execute or parse for: {}}}"',
    'format!(\n                    "{{Error in {}, select_row failed to execute or parse for: {}}}"',
    'format!(\n                        "{{Error in {}, select_row failed to execute or parse for: {}}}"',
    'format!(\n                    "{{Error in {}, select_row_bound failed to execute or parse for: {}}}"',
    'format!(\n                    "{{Error in {}, select_row_bound failed to execute or parse for: {}}}"',
    'format!(\n                        "{{Error in {}, select_row_bound failed to execute or parse for: {}}}"',
    'format!(\n                    "{{Error in {}, select_row_bound failed to execute or parse for: {}}}"',
    'format!(\n                    "{{Error in {}, select_row_bound expected single row result but found none for: {}}}"',
    'format!(\n                        "{{Error in {}, select_row_bound failed to execute or parse for: {}}}"',
    'format!(\n                        "{{Error in {}, select_row_bound expected single row result but found none for: {}}}"',
    'format!(\n                    "{{Error in {}, select_row_bound failed to execute or parse for: {}}}"',
    'format!(\n                    "{{Error in {}, select_row_bound expected single row result but found none for: {}}}"',
    'format!(\n                    "{{Error in {}, select_row_bound failed to execute or parse for: {}}}"',
    'format!(\n                    "{{Error in {}, select_row_bound expected single row result but found none for: {}}}"',
    'format!(\n                        "{{Error in {}, select_row_bound failed to execute or parse for: {}}}"',
    'format!(\n                        "{{Error in {}, select_row_bound expected single row result but found none for: {}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/diagnostics/src/diagnostics.rs'
translation = [
    'Label::new("{{No problems in workspace}}")',
    'Label::new("{{No problems}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/diagnostics/src/diagnostics_tests.rs'
translation = [
    'message: "{{value moved here}}"',
    'message: "{{unresolved name `c`}}"',
    'format!("{{diagnostic group {group_id}}}"',
    '"{{value moved here}}".to_string()',
    '"{{unresolved name `c`}}".to_string()',
    '"{{mismatched types\\nexpected `usize`, found `char`}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/diagnostics/src/items.rs'
translation = [
    'action("{{Next Diagnostic}}"',
    'action("{{Project Diagnostics}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/diagnostics/src/toolbar_controls.rs'
translation = [
    'Tooltip::text("{{Update excerpts}}"',
    '"{{Exclude Warnings}}"',
    '"{{Include Warnings}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/editor/src/blame_entry_tooltip.rs'
translation = [
    '"{{<no name>}}".to_string()',
    '"{{Error parsing date}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/editor/src/display_map.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/editor/src/display_map/inlay_map.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/editor/src/display_map/tab_map.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/editor/src/editor.rs'
translation = [
    'Tooltip::text("{{Copy diagnostic message}}"',
    'action("{{Close Diagnostics}}"',
    'format!("{{Rename: {} → {}}}"',
    'format!("{{Failed to copy permalink: {err}}}"',
    'format!("{{Failed to open permalink: {err}}}"',
    'format!(\n                "{{The remote instance of Zed does not support this yet. It must be upgraded to {}}}"',
    'format!(\n                "{{The remote instance of Zed does not support this yet. It must be upgraded to {}}}"',
    'format!(\n                                        "{{{} for {}}}"',
    'format!(\n                            "{{References to `{}`}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/editor/src/editor_tests.rs'
translation = [
    'format!("{{[{} formatted]}}"',
    '"{{Wrap the expression in an `Option::Some`}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/editor/src/element.rs'
translation = [
    'action(\n                                                    "{{Jump to File}}"',
    'action(\n                                                        "{{Expand Excerpt}}"',
    'action(\n                                                            "{{Expand Excerpt}}"',
    'action(\n                                                "{{Expand Excerpt}}"',
    'format!(\n                                                                "{{Jump to {}:L{}}}"',
    'format!(\n                                            "{{Jump to {}:L{}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/editor/src/git/blame.rs'
translation = [
    '{{Failed to blame \\"file.txt\\": failed to get blame for \\"file.txt\\"}}',
]
replace_in_file(file_path, translation)

file_path = 'crates/editor/src/highlight_matching_bracket.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/editor/src/hover_popover.rs'
translation = [
    'message: "{{A test diagnostic message.}}"',
    'action("{{Go To Diagnostic}}"',
    'format!("{{A tooltip for `{struct_label}`}}"',
    'format!("{{A tooltip for `{new_type_label}`}}"',
    'format!("{{A tooltip for {struct_label}}}"',
    'format!(\n                                    "{{A tooltip for `{new_type_label}`}}"',
    '"{{A test diagnostic message.}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/editor/src/inlay_hint_cache.rs'
translation = [
    '"{{type hint}}".to_string()',
    '"{{parameter hint}}".to_string()',
    '''"{{out of excerpt range, should be ignored}}".to_string()''',
    '"{{main hint #0}}".to_string()',
    '"{{main hint #1}}".to_string()',
    '"{{main hint #2}}".to_string()',
    '"{{main hint #3}}".to_string()',
    '"{{main hint #4}}".to_string()',
    '"{{main hint #5}}".to_string()',
    '"{{other hint #0}}".to_string()',
    '"{{other hint #1}}".to_string()',
    '"{{other hint #2}}".to_string()',
    '"{{other hint #3}}".to_string()',
    '"{{other hint #4}}".to_string()',
    '"{{other hint #5}}".to_string()',
    '"{{other hint(edited) #0}}".to_string()',
    '"{{other hint(edited) #1}}".to_string()',
    '"{{other hint(edited) #2}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/editor/src/items.rs'
translation = [
    'format!("{{No worktree for path: {path:?}}}"',
    '"{{untitled}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/editor/src/mouse_context_menu.rs'
translation = [
    'action("{{Rename Symbol}}"',
    'action("{{Go to Definition}}"',
    'action("{{Go to Type Definition}}"',
    'action("{{Go to Implementation}}"',
    'action("{{Find All References}}"',
    'action("{{Cut}}"',
    'action("{{Copy}}"',
    'action("{{Paste}}"',
    'action("{{Reveal in Finder}}"',
    'action("{{Open in Terminal}}"',
    'action(\n                    "{{Code Actions}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/editor/src/test/editor_lsp_test_context.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/editor/src/test/editor_test_context.rs'
translation = [
    '"{{Initial Editor State:}}',
]
replace_in_file(file_path, translation)

file_path = 'crates/extension/src/extension_builder.rs'
translation = [
    '''format!("{{failed to compile grammar '{grammar_name}'}}"''',
    'format!("{{failed to read output module `{}`}}"',
    'format!("{{failed to create grammar directory {}}}"',
    'format!("{{failed to save file {}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/extension/src/extension_lsp_adapter.rs'
translation = [
    'format!("{{failed to parse initialization_options from extension: {json_options}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/extension/src/extension_manifest.rs'
translation = [
    'format!("{{failed to load {extension_name} extension.json}}"',
    'format!("{{invalid extension.json for extension {extension_name}}}"',
    'format!("{{failed to load {extension_name} extension.toml}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/extension/src/extension_store.rs'
translation = [
    'format!("{{failed to load wasm extension {}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/extension/src/extension_store_test.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/extension/src/wasm_host/wit/since_v0_0_7.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/extension_api/src/extension_api.rs'
translation = [
    '"{{`language_server_command` not implemented}}".to_string()',
    '"{{`run_slash_command` not implemented}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/extension_cli/src/main.rs'
translation = [
    '''format!("{{failed to copy grammar '{}'}}"''',
    '''format!("{{failed to copy theme '{}'}}"''',
    '''format!("{{failed to copy language dir '{}'}}"''',
]
replace_in_file(file_path, translation)

file_path = 'crates/extensions_ui/src/components/extension_card.rs'
translation = [
    'Label::new("{{Overridden by dev extension.}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/extensions_ui/src/extension_suggest.rs'
translation = [
    '''format!(\n                    "{{Do you want to install the recommended '{}' extension for '{}' files?}}"''',
    '"{{dismissed}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/extensions_ui/src/extension_version_selector.rs'
translation = [
    'Label::new("{{Incompatible}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/extensions_ui/src/extensions_ui.rs'
translation = [
    'Tooltip::text("{{Show all extensions}}"',
    'Tooltip::text("{{Show installed extensions}}"',
    'Tooltip::text("{{Show not installed extensions}}"',
    'format!("{{rebuild-{}}}"',
    'format!("{{repository-{}}}"',
    'format!("{{(v{installed_version} installed)}}"',
    'format!("{{more-{}}}"',
    'format!(\n                            "{{Downloads: {}}}"',
    'format!(\n                                    "{{more-{}}}"',
    'format!(\n                                                "{{v{version} is not compatible with this version of Zed.}}"',
    'menu.entry(\n                "{{Install Another Version...}}"',
    '"{{extensions: install extension}}".to_string()',
    '"{{extensions: uninstall extension}}".to_string()',
    'Button::new("install-dev-extension", "{{Install Dev Extension}}")',
    'Button::new("filter-all", "{{All}}")',
    'Button::new("filter-installed", "{{Installed}}")',
    'Button::new("filter-not-installed", "{{Not Installed}}")',
    'Label::new("{{Extensions}}")',
    'set_placeholder_text("{{Search extensions...}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/feedback/src/feedback.rs'
translation = [
    'format!(\n        "{{https://github.com/zed-industries/zed/issues/new?assignees=&labels=admin+read%2Ctriage%2Cdefect&projects=&template=1_bug_report.yml&environment={}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/feedback/src/feedback_modal.rs'
translation = [
    'Tooltip::text("{{Submit feedback to the Zed team.}}"',
    'format!(\n                        "{{Feedback must be at least {} characters.}}"',
    'format!(\n                        "{{Characters: {}}}"',
    'Button::new("zed_repository", "{{Zed Repository}}")',
    'Button::new("cancel_feedback", "{{Cancel}}")',
    'Label::new("{{Provide an email address if you want us to be able to reply.}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/feedback/src/system_specs.rs'
translation = [
    'format!("{{OS: {} {}}}"',
    'format!("{{Memory: {}}}"',
    'format!("{{Architecture: {}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/file_finder/src/file_finder.rs'
translation = [
    '"{{Search project files...}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/file_finder/src/new_path_prompt.rs'
translation = [
    'format!("{{{} already exists. Do you want to replace it?}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/fs/src/fs.rs'
translation = [
    'format!("{{not found: {}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/fsevent/src/fsevent.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/git/src/blame.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/git/src/commit.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/git/src/repository.rs'
translation = [
    'format!("{{failed to get git working directory for file {:?}}}"',
    'format!("{{failed to get blame for {:?}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/git_hosting_providers/src/providers/bitbucket.rs'
translation = [
    'format!("{{lines-{line}}}"',
    'format!("{{lines-{start_line}:{end_line}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/git_hosting_providers/src/providers/codeberg.rs'
translation = [
    'format!("{{error fetching Codeberg commit details at {:?}}}"',
    'format!("{{L{line}}}"',
    'format!("{{L{start_line}-L{end_line}}}"',
    '"{{Codeberg}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/git_hosting_providers/src/providers/gitee.rs'
translation = [
    'format!("{{L{line}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/git_hosting_providers/src/providers/github.rs'
translation = [
    'format!("{{error fetching GitHub commit details at {:?}}}"',
    'format!("{{L{line}}}"',
    'format!("{{L{start_line}-L{end_line}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/git_hosting_providers/src/providers/gitlab.rs'
translation = [
    'format!("{{L{line}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/git_hosting_providers/src/providers/sourcehut.rs'
translation = [
    'format!("{{L{line}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/go_to_line/src/cursor_position.rs'
translation = [
    '"{{Go to Line/Column}}",',
]
replace_in_file(file_path, translation)

file_path = 'crates/go_to_line/src/go_to_line.rs'
translation = [
    'format!("{{line {} of {} (column {})}}"',
    'format!("{{Go to line {line}, column {column}}}"',
    'format!("{{Go to line {line}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/google_ai/src/google_ai.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/gpui/build.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/gpui/examples/hello_world.rs'
translation = [
    'format!("{{Hello, {}!}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/gpui/examples/image/image.rs'
translation = [
    'action("{{Quit}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/gpui/examples/set_menus.rs'
translation = [
    'action("{{Quit}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/gpui/examples/window_positioning.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/gpui/src/action.rs'
translation = [
    'format!("{{Attempting to build action {}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/gpui/src/color.rs'
translation = [
    '''format!("{{{INVALID_UNICODE}: r component of #rgb/#rgba for value: '{value}'}}"''',
    '''format!("{{{INVALID_UNICODE}: g component of #rgb/#rgba for value: '{value}'}}"''',
    '''format!("{{{INVALID_UNICODE}: b component of #rgb/#rgba for value: '{value}'}}"''',
    '''format!("{{{INVALID_UNICODE}: a component of #rgba for value: '{value}'}}"''',
    '''format!(\n                            "{{{}: r component of #rrggbb/#rrggbbaa for value: '{}'}}"''',
    '''format!(\n                            "{{{INVALID_UNICODE}: g component of #rrggbb/#rrggbbaa for value: '{value}'}}"''',
    '''format!(\n                            "{{{INVALID_UNICODE}: b component of #rrggbb/#rrggbbaa for value: '{value}'}}"''',
    '''format!(\n                                "{{{INVALID_UNICODE}: a component of #rrggbbaa for value: '{value}'}}"''',
]
replace_in_file(file_path, translation)

file_path = 'crates/gpui/src/elements/div.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/gpui/src/executor.rs'
translation = [
    '{{backtrace of waiting future:}}',
    '{{waiting on:}}',
]
replace_in_file(file_path, translation)

file_path = 'crates/gpui/src/platform/cosmic_text/text_system.rs'
translation = [
    'format!("{{no image for {params:?} in font {font:?}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/gpui/src/platform/linux/platform.rs'
translation = [
    'title("{{Select new path}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/gpui/src/platform/linux/wayland/clipboard.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/gpui/src/platform/mac.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/gpui/src/platform/mac/events.rs'
translation = [
    '"{{space}}".to_string()',
    '"{{backspace}}".to_string()',
    '"{{enter}}".to_string()',
    '"{{escape}}".to_string()',
    '"{{tab}}".to_string()',
    '"{{up}}".to_string()',
    '"{{down}}".to_string()',
    '"{{left}}".to_string()',
    '"{{right}}".to_string()',
    '"{{pageup}}".to_string()',
    '"{{pagedown}}".to_string()',
    '"{{home}}".to_string()',
    '"{{end}}".to_string()',
    '"{{delete}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/gpui/src/platform/mac/platform.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/gpui/src/platform/test/platform.rs'
translation = [
    'format!("{{PROMPT: {:?} {:?}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/gpui/src/platform/windows/events.rs'
translation = [
    '"{{space}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/gpui/src/platform/windows/platform.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/gpui/src/platform/windows/util.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/gpui/src/view.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/gpui_macros/src/style_helpers.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/html_to_markdown/src/structure/wikipedia.rs'
translation = [
    'title="{{Browser engine}}"',
    'title="{{Servo (software)}}"',
    'title="{{Region-based memory management}}"',
    'title="{{Cyclone (programming language)}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/http/src/github.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/http/src/http.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/inline_completion_button/src/inline_completion_button.rs'
translation = [
    'action("{{Sign Out}}"',
    '''format!("{{Copilot can't be started: {}}}"''',
    'format!("{{Supermaven error: {}}}"',
    'format!(\n                    "{{{} Inline Completions for {}}}"',
    'format!(\n                    "{{{} Inline Completions for This Path}}"',
    'menu.entry("{{Sign In}}"',
    '"{{Supermaven is ready}}".to_string()',
    '"{{Supermaven needs activation}}".to_string()',
    '"{{Supermaven initializing}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/install_cli/src/install_cli.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/journal/src/journal.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/language/src/buffer.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/language/src/buffer_tests.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/language/src/language.rs'
translation = [
    '"{{Plain Text}}" =>',
    '"{{Plain Text}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/language/src/language_registry.rs'
translation = [
    'format!("{{language for file path {}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/language/src/markdown.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/language/src/syntax_map/syntax_map_tests.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/language_selector/src/active_buffer_language.rs'
translation = [
    'Tooltip::text("{{Select Language}}"',
    '"{{Unknown}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/language_tools/src/lsp_log.rs'
translation = [
    'format!("{{stderr: {}}}"',
    '"{{supplementary}}".to_string()',
    'Button::new("clear_log_button", "{{Clear}}")',
    'Label::new("{{LSP Logs}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/language_tools/src/lsp_log_tests.rs'
translation = [
    'message: "{{hello from the server}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/language_tools/src/syntax_tree_view.rs'
translation = [
    'Label::new("{{Syntax Tree}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/languages/src/bash.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/languages/src/c.rs'
translation = [
    '"{{no asset found matching}}',
]
replace_in_file(file_path, translation)

file_path = 'crates/languages/src/go.rs'
translation = [
    '''format!("{{failed to parse golps version output '{version_stdout}'}}"''',
]
replace_in_file(file_path, translation)

file_path = 'crates/languages/src/lib.rs'
translation = [
    'format!("{{failed to load config.toml for language {name:?}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/languages/src/python.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/languages/src/rust.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/languages/src/tailwind.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/languages/src/typescript.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/languages/src/vtsls.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/live_kit_client/build.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/live_kit_server/src/api.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/lsp/src/lsp.rs'
translation = [
    'message: "{{ok}}"',
    'format!(\n                "{{failed to spawn command. path: {:?}, working directory: {:?}, args: {:?}}}"',
    '"{{edit}}".to_string()',
    '"{{command}}".to_string()',
    '"{{documentation}}".to_string()',
    '"{{ok}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/markdown/src/markdown.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/markdown_preview/src/markdown_parser.rs'
translation = [
    '"{{Some bostrikethroughld text}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/markdown_preview/src/markdown_preview_view.rs'
translation = [
    'format!("{{Preview {}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/markdown_preview/src/markdown_renderer.rs'
translation = [
    'format!("{{{}-click to toggle the checkbox}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/media/build.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/multi_buffer/src/multi_buffer.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/node_runtime/src/node_runtime.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/ollama/src/ollama.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/open_ai/src/open_ai.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/outline/src/outline.rs'
translation = [
    '"{{Search buffer symbols...}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/outline_panel/src/outline_panel.rs'
translation = [
    'action("{{Reveal in Finder}}"',
    'action("{{Open in Terminal}}"',
    'action("{{Unfold Directory}}"',
    'action("{{Fold Directory}}"',
    'action("{{Copy Path}}"',
    'action("{{Copy Relative Path}}"',
    'format!(\n            "{{Lines {}-{}}}"',
    '"{{Untitled}}".to_string()',
    '"{{Unknown buffer}}".to_string()',
    'Label::new("{{No editor outlines available}}")',
    '"{{Outline Panel}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/prettier/src/prettier.rs'
translation = [
    'format!("{{failed to get metadata for initial path {path_to_check:?}}}"',
    'format!("{{empty metadata for initial path {path_to_check:?}}}"',
    'format!("{{fetching metadata for {possible_node_modules_location:?}}}"',
    'format!("{{fetching metadata for package json {possible_package_json:?}}}"',
    'format!("{{reading {possible_package_json:?} file contents}}"',
    'format!("{{parsing {possible_package_json:?} file contents}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/project/src/lsp_command.rs'
translation = [
    'format!("{{incorrect proto inlay hint message: non-json resolve state {lsp_resolve_state:?}}}"',
    'format!(\n                        "{{No lsp resolve data for the hint that can be resolved: {message_hint:?}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/project/src/prettier_support.rs'
translation = [
    'format!("{{prettier at {path:?}}}"',
    'format!("{{{} failed to format buffer}}"',
    'format!("{{prettier ({name})}}"',
    'format!("{{prettier ({})}}"',
    'format!("{{fetching latest npm version for package {returned_package_name}}}"',
    'format!("{{fetching FS metadata for default prettier dir {default_prettier_dir:?}}}"',
    'format!("{{creating default prettier dir {default_prettier_dir:?}}}"',
    'format!(\n            "{{writing {} file at {prettier_wrapper_path:?}}}"',
    '"{{default prettier instance}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/project/src/project.rs'
translation = [
    'format!("{{No worktree for entry {entry_id:?}}}"',
    'format!("{{Missing worktree for id {source}}}"',
    'format!("{{Missing worktree for id {destination}}}"',
    'format!("{{loading file and FS metadata for {path:?}}}"',
    'format!("{{Failed to blame {:?}}}"',
    'format!("{{waiting for version for buffer {}}}"',
    'format!("{{fetching fs metadata for {ignored_abs_path:?}}}"',
    'format!("{{listing ignored path {ignored_abs_path:?}}}"',
    'format!("{{Opening ignored path {ignored_abs_path:?}}}"',
    'format!("{{failed to determine load login shell environment in {worktree_abs_path:?}}}"',
    'format!(\n                "{{No worktree for path {project_path:?}}}"',
    'format!(\n                                "{{Language server {name} (id {server_id}) status update: {message}}}"',
    'format!(\n                        "{{failed to format via external command {:?}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/project/src/project_tests.rs'
translation = [
    'title: "{{The code action}}"',
    'title: "{{The command}}"',
    'message: "{{the message}}"',
    'message: "{{original diagnostic}}"',
    'format!("{{{name} code action}}"',
    '"{{the message}}".to_string()',
    '"{{disk}}".to_string()',
    '"{{original diagnostic}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/project/src/search_history.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/project/src/task_inventory.rs'
translation = [
    '"{{oneshot}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/project/src/terminals.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/project_panel/src/project_panel.rs'
translation = [
    'action("{{Copy Relative Path}}"',
    'action("{{Search Inside}}"',
    'action("{{New File}}"',
    'action("{{New Folder}}"',
    'action("{{Reveal in Finder}}"',
    'action("{{Open in Terminal}}"',
    'action("{{Find in Folder…}}"',
    'action("{{Unfold Directory}}"',
    'action("{{Fold Directory}}"',
    'action("{{Cut}}"',
    'action("{{Copy}}"',
    'action("{{Duplicate}}"',
    'action("{{Paste}}"',
    'action("{{Copy Path}}"',
    'action("{{Rename}}"',
    'action("{{Trash}}"',
    'action("{{Delete}}"',
    'action("{{Collapse All}}"',
    'action(\n                                            "{{Add Folder to Project…}}"',
    'format!("{{.. {} files not shown}}"',
    'format!("{{A file or folder with name {filename} already exists in the destination folder. Do you want to replace it?}}"',
    'format!("{{{path} • Symbolic Link}}"',
    '''format!("{{[EDITOR: '{}']}}"''',
    '''format!("{{[PROCESSING: '{}']}}"''',
    'format!(\n                                            "{{{} is not shared by the host. This could be because it has been marked as `private`}}"',
    '"{{Disconnected from remote project}}".to_string()',
    '"{{excluded_dir}}".to_string()',
    'Button::new("open_project", "{{Open a project}}")',
    '{{Created an excluded directory at {abs_path:?}.\\nAlter `file_scan_exclusions` in the settings to show it in the panel}}',
    '{{Do you want to {} the following {} files?\\n{}}}',
    '"{{Project Panel}}"',
    '"{{Remove from Project}}",',
    '"{{Failed to open file}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/project_symbols/src/project_symbols.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/proto/src/error.rs'
translation = [
    'format!("{{You need to be on the {} release channel.}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/quick_action_bar/src/quick_action_bar.rs'
translation = [
    'Tooltip::text("{{Selection Controls}}"',
    'Tooltip::text("{{Editor Controls}}"',
    'action("{{Select All}}"',
    'action("{{Expand Selection}}"',
    'action("{{Shrink Selection}}"',
    'action("{{Add Cursor Above}}"',
    'action("{{Add Cursor Below}}"',
    'action("{{Go to Symbol}}"',
    'action("{{Go to Line/Column}}"',
    'action("{{Next Problem}}"',
    'action("{{Previous Problem}}"',
    'action("{{Next Hunk}}"',
    'action("{{Previous Hunk}}"',
    'action("{{Move Line Up}}"',
    'action("{{Move Line Down}}"',
    'action("{{Duplicate Selection}}"',
    'action(\n                                    "{{Select Next Occurrence}}"',
    'menu.toggleable_entry(\n                                    "{{Show Inlay Hints}}"',
    'menu.toggleable_entry(\n                                "{{Show Git Blame Inline}}"',
    'menu.toggleable_entry(\n                                "{{Show Selection Menu}}"',
    '"{{Buffer Search}}",',
    '"{{toggle inline assistant}}",',
    '"{{Inline Assist}}",',
]
replace_in_file(file_path, translation)

file_path = 'crates/recent_projects/src/dev_servers.rs'
translation = [
    'Tooltip::text("{{Reconnect}}"',
    'Tooltip::text("{{Edit dev server}}"',
    'Tooltip::text("{{Remove dev server}}"',
    'Tooltip::text("{{Delete remote project}}"',
    'Tooltip::text("{{Register a new dev server}}"',
    'format!("{{The path `{}` does not exist on the server.}}"',
    'format!(\n                        "{{Project {} already exists for this dev server.}}"',
    'Button::new("create-dev-server", "{{Done}}")',
    'Button::new("register-dev-server-button", "{{New Server}}")',
    'Label::new("{{Open folder…}}")',
    'Label::new("{{Connect via SSH (default)}}")',
    'Label::new("{{Manual Setup}}")',
    'Label::new("{{Not connected}}")',
    'Label::new("{{🎊 Connection established!}}")',
    "{{Please log into '{}'. If you don't yet have zed installed, run:\\n```\\ncurl https://zed.dev/install.sh | bash\\n```\\nThen to start zed in headless mode:\\n```\\nzed --dev-server-token {}\\n```}}",
    "{{Please wait while we connect over SSH.\\n\\nIf you run into problems, please [file a bug](https://github.com/zed-industries/zed), and in the meantime try using manual setup.}}",
]
replace_in_file(file_path, translation)

file_path = 'crates/recent_projects/src/disconnected_overlay.rs'
translation = [
    'Button::new("close-window", "{{Close Window}}")',
    'Button::new("reconnect", "{{Reconnect}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/recent_projects/src/recent_projects.rs'
translation = [
    'Tooltip::text("{{Delete from Recent Projects...}}"',
    'format!("{{Cannot connect to {}. To debug open the remote project settings.}}"',
    'format!(\n            "{{{reuse_window} reuses this window, {create_window} opens a new one}}"',
    '"{{fake candidate}}".to_string()',
    'Label::new("{{New remote project…}}")',
    'Label::new("{{Open local folder…}}")',
    '"{{Recently opened projects will show up here}}".into()',
    '"{{No matches}}".into()',
    '{{App state not found}}',
    '{{After inserting more text into the editor without saving, we should have a dirty project}}',
    '{{Should have no pending prompt on dirty project before opening the new recent project}}',
    '{{Should remove the modal after selecting new recent project}}',
    '{{Dirty workspace should prompt before opening the new recent project}}',
    '{{Should have no pending prompt after cancelling}}',
    '{{Should be in the same dirty project after cancelling}}',
]
replace_in_file(file_path, translation)

file_path = 'crates/repl/src/outputs.rs'
translation = [
    'format!("{{Failed to load image: {}}}"',
    '"{{Unsupported media type}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/repl/src/runtimes.rs'
translation = [
    'format!("{{kernel-zed-{}.json}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/rich_text/src/rich_text.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/rpc/src/peer.rs'
translation = [
    'format!(\n                "{{message {} was not handled}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/rustdoc/src/indexer.rs'
translation = [
    'format!("{{failed to fetch {item:?}}}"',
    'format!(\n                            "{{failed to fetch {item:?}: {history:?}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/rustdoc/src/item.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/rustdoc/src/store.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/rustdoc/src/to_markdown.rs'
translation = [
    'title="{{Copy item path to clipboard}}"',
    'title="{{collapse all docs}}"',
    'title="{{Available on crate feature `form` only}}"',
    'title="{{Available on crate feature `json` only}}"',
    'title="{{Available on crate feature `tokio` and (crate features `http1` or `http2`) only}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/search/src/buffer_search.rs'
translation = [
    'action("{{Toggle replace}}"',
    'action("{{Toggle search selection}}"',
    'action("{{Select all matches}}"',
    'action("{{Replace next}}"',
    'action("{{Replace all}}"',
    'action("{{Close search bar}}"',
    '"{{Select previous match}}",',
    '"{{Select next match}}",',
    'set_placeholder_text("{{Search}}"',
    'set_placeholder_text("{{Replace with...}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/search/src/mode.rs'
translation = [
    'format!("{{Activate {} Mode}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/search/src/project_search.rs'
translation = [
    'action("{{Toggle filters}}"',
    'action("{{Toggle replace}}"',
    'action("{{Go to previous match}}"',
    'action("{{Go to next match}}"',
    'action("{{Replace next match}}"',
    'action("{{Replace all matches}}"',
    'Label::new("{{Searching...}}")',
    'Label::new("{{No results}}")',
    'Label::new("{{Search all files}}")',
    'Label::new("{{Search limit reached}}")',
    'set_placeholder_text("{{Search all files..}}"',
    'set_placeholder_text("{{Replace in project..}}"',
    'set_placeholder_text("{{Include: crates/**/*.toml}}"',
    'set_placeholder_text("{{Exclude: vendor/*, *.lock}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/search/src/search.rs'
translation = [
    'format!("{{Toggle {}}}"',
    '"{{whole word}}",',
    '"{{match case}}",',
    '"{{include Ignored}}",',
    '"{{regular expression}}",',
    '"{{{:?} is not a named SearchOption}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/search/src/search_bar.rs'
translation = [
    'format!("{{search-nav-button-{}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/semantic_index/src/chunking.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/semantic_index/src/embedding/cloud.rs'
translation = [
    'format!("{{server did not return an embedding for {:?}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/semantic_index/src/project_index_debug_view.rs'
translation = [
    'format!(\n                        "{{chunk {} of {}. length: {}}}"',
    'Label::new("{{Project Index (Debug)}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/semantic_index/src/semantic_index.rs'
translation = [
    'format!("{{failed to read path {entry_abs_path:?}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/semantic_version/src/semantic_version.rs'
translation = [
    '{{Invalid version string}}',
]
replace_in_file(file_path, translation)

file_path = 'crates/settings/src/keymap_file.rs'
translation = [
    'format!(\n                            "{{invalid binding value for keystroke {keystroke}, context {context:?}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/settings/src/settings_file.rs'
translation = [
    'format!("{{Failed to canonicalize settings path {:?}}}"',
    'format!("{{Failed to write settings to file {:?}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/settings/src/settings_store.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/sqlez/src/bindable.rs'
translation = [
    'format!("{{Failed to bind bool at index {start_index}}}"',
    'format!("{{Failed to read bool at index {start_index}}}"',
    'format!("{{Failed to bind &[u8] at index {start_index}}}"',
    'format!("{{Failed to bind &[u8; C] at index {start_index}}}"',
    'format!("{{Failed to bind Vec<u8> at index {start_index}}}"',
    'format!("{{Failed to read Vec<u8> at index {start_index}}}"',
    'format!("{{Failed to bind f64 at index {start_index}}}"',
    'format!("{{Failed to parse f64 at index {start_index}}}"',
    'format!("{{Failed to parse f32 at index {start_index}}}"',
    'format!("{{Failed to bind i32 at index {start_index}}}"',
    'format!("{{Failed to bind i64 at index {start_index}}}"',
    'format!("{{Failed to bind usize at index {start_index}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/sqlez/src/connection.rs'
translation = [
    '"{{test}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/sqlez/src/migrations.rs'
translation = [
    '{{Prepare call failed for query:}}',
]
replace_in_file(file_path, translation)

file_path = 'crates/sqlez/src/savepoint.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/sqlez/src/statement.rs'
translation = [
    'format!("{{Failed to bind value at index {index}}}"',
    'format!("{{Failed to read blob at index {index}}}"',
    'format!("{{Failed to read length of blob at index {index}}}"',
    'format!("{{Failed to read double at index {index}}}"',
    'format!("{{Failed to read int at index {index}}}"',
    'format!("{{Failed to read i64 at index {index}}}"',
    'format!("{{Failed to read text from column {index}}}"',
    'format!("{{Failed to read text length at {index}}}"',
    '{{Prepare call failed for query:}}',
]
replace_in_file(file_path, translation)

file_path = 'crates/sqlez/src/thread_safe_connection.rs'
translation = [
    'format!(\n                            "{{Db initialize query failed to execute: {}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/sqlez_macros/src/sqlez_macros.rs'
translation = [
    '{{Sql Error: {}\\nFor Query: {}}}',
]
replace_in_file(file_path, translation)

file_path = 'crates/story/src/story.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/storybook/src/app_menus.rs'
translation = [
    'action("{{Quit}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/storybook/src/stories/cursor.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/storybook/src/stories/kitchen_sink.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/storybook/src/stories/overflow_scroll.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/storybook/src/stories/scroll.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/storybook/src/stories/with_rem_size.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/storybook/src/story_selector.rs'
translation = [
    '''format!("{{story not found for component '{story}'}}"''',
]
replace_in_file(file_path, translation)

file_path = 'crates/storybook/src/storybook.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/supermaven/src/supermaven.rs'
translation = [
    'format!("{{failed to deserialize line from stdout: {:?}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/supermaven_api/src/supermaven_api.rs'
translation = [
    'format!("{{Unable to create file at {:?}}}"',
    'format!("{{Unable to write binary to file at {:?}}}"',
    'format!(\n                    "{{Could not create Supermaven Agent Directory at {:?}}}"',
    '"{{Unable to get Supermaven API Key}}".to_string()',
    '"{{Unable to parse Supermaven user response}}".to_string()',
    '"{{Unable to create Supermaven API Key}}".to_string()',
    '"{{Unable to parse Supermaven API Key response}}".to_string()',
    '"{{Unable to delete Supermaven User}}".to_string()',
    '"{{Unable to acquire Supermaven Agent}}".to_string()',
    '"{{Unable to parse Supermaven Agent response}}".to_string()',
    '"{{Unable to download Supermaven Agent}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/tab_switcher/src/tab_switcher.rs'
translation = [
    'Tooltip::text("{{Close}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/task/src/lib.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/task/src/task_template.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/task/src/vscode_format.rs'
translation = [
    '"{{Build Extension in Background}}".to_string()',
    '"{{Build Extension}}".to_string()',
    '"{{Build Server}}".to_string()',
    '"{{Build Server (Release)}}".to_string()',
    '"{{Pretest}}".to_string()',
    '"{{pretest}}".to_string()',
    '"{{Build Server and Extension}}".to_string()',
    '"{{Build Server (Release) and Extension}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/tasks_ui/src/modal.rs'
translation = [
    'Tooltip::text("{{Delete previously scheduled task}}"',
    '"{{example task}}".to_string()',
    '"{{hello from …th.odd_extension:1:1}}".to_string()',
    '"{{opened now: /dir}}".to_string()',
    '"{{hello from …ithout_extension:2:3}}".to_string()',
    '"{{Task without variables}}".to_string()',
    '"{{npm run clean}}".to_string()',
    '"{{TypeScript task from file $ZED_FILE}}".to_string()',
    '"{{npm run build}}".to_string()',
    '"{{Another task from file $ZED_FILE}}".to_string()',
    '"{{npm run lint}}".to_string()',
    '"{{Rust task}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/terminal/src/mappings/keys.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/terminal/src/mappings/mouse.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/terminal/src/terminal.rs'
translation = [
    'format!("{{{TASK_DELIMITER}Task `{escaped_full_label}` finished successfully}}"',
    'format!("{{{TASK_DELIMITER}Task `{escaped_full_label}` finished with non-zero error code: {error_code}}}"',
    'format!("{{{TASK_DELIMITER}Task `{escaped_full_label}` finished}}"',
    '''format!("{{{TASK_DELIMITER}Command: '{escaped_command_label}'}}"''',
    '"{{<none specified, could not find home directory>}}".to_string()',
    '"{{<system shell>}}".to_string()',
    '"{{<system defined shell>}}".to_string()',
    '"{{Terminal}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/terminal_view/src/terminal_panel.rs'
translation = [
    'Tooltip::text("{{New...}}"',
    'action(\n                                        "{{New Terminal}}"',
    'Some("{{Terminal Panel}}")',
    # maybe a typo here
    '"{{TerminalPanel}}"',
    '"{{Spawn task}}",',
    '"{{Zoom Out}}"',
    '"{{Zoom In}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/terminal_view/src/terminal_view.rs'
translation = [
    'Tooltip::text("{{Rerun task}}"',
    'action("{{Clear}}"',
    'action("{{Close}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/theme/src/default_theme.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/theme/src/one_themes.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/theme/src/registry.rs'
translation = [
    'format!("{{reading themes from {themes_path:?}}}"',
    '{{failed to parse theme at path}}',
]
replace_in_file(file_path, translation)

file_path = 'crates/theme/src/settings.rs'
translation = [
    '"{{compact}}".to_string()',
    '"{{default}}".to_string()',
    '"{{comfortable}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/theme/src/styles/stories/color.rs'
translation = [
    'title("{{Colors}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/theme/src/styles/syntax.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/theme_importer/src/color.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/theme_importer/src/main.rs'
translation = [
    'format!("{{failed to parse theme {theme_file_path:?}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/theme_importer/src/vscode/converter.rs'
translation = [
    '"{{no identifier}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/time_format/src/time_format.rs'
translation = [
    'format!("{{Today at {}}}"',
    'format!("{{Yesterday at {}}}"',
    'format!("{{{} minutes ago}}"',
    'format!("{{{} hours ago}}"',
    'format!("{{{} days ago}}"',
    'format!("{{{} weeks ago}}"',
    'format!("{{{} months ago}}"',
    'format!("{{{} years ago}}"',
    '"{{Just now}}".to_string()',
    '"{{1 minute ago}}".to_string()',
    '"{{1 hour ago}}".to_string()',
    '"{{Today}}".to_string()',
    '"{{Yesterday}}".to_string()',
    '"{{1 week ago}}".to_string()',
    '"{{1 month ago}}".to_string()',
    '"{{1 year ago}}".to_string()',
    '"{{4 weeks ago}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/ui/src/components/button/button.rs'
translation = [
    'Tooltip::text("{{This is a tooltip}}"',
    'Button::new("button_id", "{{Click me!}}")',
    'Button::new("button_id", "{{Click me!}}")',
    'Button::new("button_id", "{{Click me!}}")',
    'Button::new("button_id", "{{Click me!}}")',
    'Button::new("button_id", "{{Click me!}}")',
    'Button::new("button_id", "{{Click me!}}")',
    'Button::new("button_id", "{{Click me!}}")',
    'Button::new("button_id", "{{Click me!}}")',
    'Button::new("button_id", "{{Click me!}}")',
    'Button::new("button_id", "{{Click me!}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/ui/src/components/button/icon_button.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/ui/src/components/checkbox/checkbox.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/ui/src/components/checkbox/checkbox_with_label.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/ui/src/components/context_menu.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/ui/src/components/keybinding.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/ui/src/components/label/label.rs'
translation = [
    'Label::new("{{Hello, World!}}")',
    'Label::new("{{Delete}}")',
    'Label::new("{{Deleted}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/ui/src/components/list/list.rs'
translation = [
    'message: "{{No items}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/ui/src/components/modal.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/ui/src/components/stories/button.rs'
translation = [
    'Button::new("default_filled", "{{Click me}}")',
    'Button::new("selected_filled", "{{Click me}}")',
    'Button::new("selected_label_filled", "{{Click me}}")',
    'Button::new("filled_with_label_color", "{{Click me}}")',
    'Button::new("filled_with_icon", "{{Click me}}")',
    'Button::new("filled_and_selected_with_icon", "{{Click me}}")',
    'Button::new("default_subtle", "{{Click me}}")',
    'Button::new("default_transparent", "{{Click me}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/ui/src/components/stories/context_menu.rs'
translation = [
    'action("{{Print current time}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/ui/src/components/stories/icon_button.rs'
translation = [
    'Tooltip::text("{{Open messages}}"',
    'Tooltip::text("{{Toggle inlay hints}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/ui/src/components/stories/label.rs'
translation = [
    'Label::new("{{Hello, world!}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/ui/src/components/stories/tab_bar.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/ui/src/components/stories/toggle_button.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/ui/src/components/stories/tool_strip.rs'
translation = [
    'Tooltip::text("{{Example tool}}"',
    'Tooltip::text("{{Example tool 2}}"',
    'Tooltip::text("{{Example tool 3}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/ui/src/components/tab.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/ui/src/components/tool_strip.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/ui/src/utils/format_distance.rs'
translation = [
    'format!("{{{} minutes}}"',
    'format!("{{{} hours}}"',
    'format!("{{about {} hours}}"',
    'format!("{{{} days}}"',
    'format!("{{{} months}}"',
    'format!("{{{} years}}"',
    'format!("{{about {} years}}"',
    'format!("{{over {} years}}"',
    'format!("{{almost {} years}}"',
    '"{{1 minute}}".to_string()',
    '"{{1 day}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/util/src/paths.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/util/src/util.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/vcs_menu/src/lib.rs'
translation = [
    '''format!("{{Failed to checkout branch '{current_pick}', check for conflicts or unstashed files}}"''',
    '''format!("{{Failed to create branch '{current_pick}', check for conflicts or unstashed files}}"''',
    '''format!("{{Failed to check branch '{current_pick}', check for conflicts or unstashed files}}"''',
    'Button::new("branch-picker-create-branch-button", "{{Create branch}}")',
    'Label::new("{{Recent Branches}}")',
    'Label::new("{{Branches}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/vim/src/command.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/vim/src/mode_indicator.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/vim/src/normal.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/vim/src/normal/change.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/vim/src/normal/increment.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/vim/src/normal/mark.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/vim/src/normal/paste.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/vim/src/normal/repeat.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/vim/src/normal/yank.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/vim/src/object.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/vim/src/surrounds.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/vim/src/test.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/vim/src/test/neovim_backed_test_context.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/vim/src/test/neovim_connection.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/vim/src/vim.rs'
translation = [
    'title: "{{Default Vim Bindings}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/welcome/src/welcome.rs'
translation = [
    '"{{welcome page: change theme}}".to_string()',
    '"{{welcome page: change keymap}}".to_string()',
    '"{{welcome page: install cli}}".to_string()',
    '"{{welcome page: sign in to copilot}}".to_string()',
    '"{{welcome page: open extensions}}".to_string()',
    '"{{welcome page: toggle vim}}".to_string()',
    '"{{welcome page: toggle metric telemetry}}".to_string()',
    '"{{welcome page: toggle diagnostic telemetry}}".to_string()',
    '"{{welcome page: close}}".to_string()',
    'Button::new("choose-theme", "{{Choose a theme}}")',
    'Button::new("choose-keymap", "{{Choose a keymap}}")',
    'Button::new("install-cli", "{{Install the CLI}}")',
    'Button::new("sign-in-to-copilot", "{{Sign in to GitHub Copilot}}")',
    'Button::new("explore extensions", "{{Explore extensions}}")',
    'Label::new("{{Code at the speed of thought}}")',
    'Label::new("{{Enable vim mode}}")',
    'Label::new("{{Send anonymous usage data}}")',
    'Label::new("{{Send crash reports}}")',
    'Label::new("{{Welcome to Zed!}}")',
]
replace_in_file(file_path, translation)

file_path = 'crates/workspace/src/dock.rs'
translation = [
    'format!("{{Close {} dock}}"',
    'format!("{{Dock {}}}"',
    '"{{left}}",',
    '"{{bottom}}",',
    '"{{right}}",',
]
replace_in_file(file_path, translation)

file_path = 'crates/workspace/src/notifications.rs'
translation = [
    'Tooltip::text("{{Copy}}"',
    'format!("{{Error: {err:#}}}"',
    'format!("{{{err}. Please try again.}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/workspace/src/pane.rs'
translation = [
    'Tooltip::text("{{New...}}"',
    'Tooltip::text("{{Split Pane}}"',
    'action("{{New File}}"',
    'action("{{New Terminal}}"',
    'action("{{Split Right}}"',
    'action("{{Split Left}}"',
    'action("{{Split Up}}"',
    'action("{{Split Down}}"',
    'action("{{Go Back}}"',
    'action("{{Go Forward}}"',
    'action(\n                                            "{{Open File}}"',
    'action(\n                                            "{{Search Project}}"',
    'action(\n                                            "{{Search Symbols}}"',
    'format!("{{.. {} files not shown}}"',
    'format!("{{{path} contains unsaved edits. Do you want to save it?}}"',
    'format!(\n                "{{Do you want to save changes to the following {} files?}}"',
    'menu.entry(\n                                    "{{Open in Terminal}}"',
    'Label::new("{{Open a file or project to get started.}}")',
    '"{{Zoom Out}}"',
    '"{{Zoom In}}"',
    '"{{.. 1 file not shown}}"',
    '"{{Save all}}"',
    '"{{Discard all}}"',
    '"{{Cancel}}"',
    '"{{This file has changed on disk since you started editing it. Do you want to overwrite it?}}"',
    '"{{Overwrite}}"',
    '"{{Discard}}"',
    '"{{Save}}"',
    '''"{{Don't Save}}"''',
    '"{{save modal was not present in spawned modals after awaiting for its answer}}"',
    '"{{Close}}",',
    '"{{Close Others}}",',
    '"{{Close Left}}",',
    '"{{Close Right}}",',
    '"{{Close Clean}}",',
    '"{{Close All}}",',
    '"{{Reveal In Project Panel}}",',
    '"{{Cannot drop files on a remote project}}"',
    '.unwrap_or("{{This buffer}}");',
]
replace_in_file(file_path, translation)

file_path = 'crates/workspace/src/pane_group.rs'
translation = [
    'format!(\n                                        "{{{} is in an unshared pane}}"',
    'format!(\n                                    "{{Follow {} to their active project}}"',
    'format!(\n                            "{{{} is viewing an unshared Zed project}}"',
    'format!(\n                            "{{{} is viewing a window outside of Zed}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/workspace/src/shared_screen.rs'
translation = [
    '''format!("{{{}'s screen}}"''',
]
replace_in_file(file_path, translation)

file_path = 'crates/workspace/src/workspace.rs'
translation = [
    'format!("{{Failed to read WorkspaceId at index {start_index}}}"',
    'format!("{{{}: open}}"',
    'format!("{{open abs path {abs_path:?} task spawn}}"',
    'format!("{{open abs path {abs_path:?} task join}}"',
    '"{{open project}}".to_string()',
    '"{{empty project}}".to_string()',
    '{{{}\\n\\nPlease try again.}}',
    '"{{Do you want to leave the current call?}}",',
    '"{{Close window and hang up}}"',
    '"{{Cancel}}"',
    '"{{Save all}}"',
    '"{{Discard all}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/worktree/src/worktree.rs'
translation = [
    'format!("{{absolutizing {path:?}}}"',
    'format!("{{absolutizing {new_path:?}}}"',
    'format!("{{loading file and FS metadata for {abs_path:?}}}"',
    'format!("{{Loading metadata for excluded file {abs_path:?}}}"',
    'format!("{{Excluded file {abs_path:?} got removed during loading}}"',
    'format!("{{absolutizing path {path:?}}}"',
    'format!("{{creating directory {task_abs_path:?}}}"',
    'format!("{{creating file {task_abs_path:?}}}"',
    'format!("{{Fetching metadata after saving the excluded buffer {abs_path:?}}}"',
    'format!("{{Excluded buffer {path:?} got removed during saving}}"',
    'format!("{{Renaming {abs_old_path:?} into {abs_new_path:?}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/worktree/src/worktree_settings.rs'
translation = [
    'format!("{{Failed to parse globs from {}}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/worktree/src/worktree_tests.rs'
translation = [
    '"{{build_output}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/zed/src/main.rs'
translation = [
    'format!("{{Failed to create themes dir at path {themes_dir:?}}}"',
    '{{{}\\n\\nFor help resolving this, please open an issue on https://github.com/zed-industries/zed}}',
]
replace_in_file(file_path, translation)

file_path = 'crates/zed/src/reliability.rs'
translation = []
replace_in_file(file_path, translation)

file_path = 'crates/zed/src/zed.rs'
translation = [
    'action("{{New Window}}"',
    'format!("{{language name {name}}}"',
    'format!(\n                                    "{{Installed `zed` to {}. You can launch {} from your terminal.}}"',
    'format!(\n                                    "{{zed:// links will now open in {}.}}"',
    'format!(\n                                            "{{Unable to access/open log file at path {:?}}}"',
    'format!(\n                                "{{Last {} lines in {}}}"',
    '"{{// No data has been collected yet}}".to_string()',
    '"{{excluded_dir}}".to_string()',
]
replace_in_file(file_path, translation)

file_path = 'crates/zed/src/zed/app_menus.rs'
translation = [
    'action("{{About Zed…}}"',
    'action("{{Check for Updates}}"',
    'action("{{Open Settings}}"',
    'action("{{Open Key Bindings}}"',
    'action("{{Open Default Settings}}"',
    'action("{{Open Default Key Bindings}}"',
    'action("{{Open Local Settings}}"',
    'action("{{Select Theme...}}"',
    'action("{{Extensions}}"',
    'action("{{Install CLI}}"',
    'action("{{Hide Zed}}"',
    'action("{{Hide Others}}"',
    'action("{{Show All}}"',
    'action("{{Quit}}"',
    'action("{{New}}"',
    'action("{{New Window}}"',
    'action("{{Open…}}"',
    'action("{{Add Folder to Project…}}"',
    'action("{{Save}}"',
    'action("{{Save As…}}"',
    'action("{{Save All}}"',
    'action("{{Close Window}}"',
    'action("{{Undo}}"',
    'action("{{Redo}}"',
    'action("{{Cut}}"',
    'action("{{Copy}}"',
    'action("{{Paste}}"',
    'action("{{Find}}"',
    'action("{{Find In Project}}"',
    'action("{{Expand Selection}}"',
    'action("{{Shrink Selection}}"',
    'action("{{Add Cursor Above}}"',
    'action("{{Add Cursor Below}}"',
    'action("{{Move Line Up}}"',
    'action("{{Move Line Down}}"',
    'action("{{Duplicate Selection}}"',
    'action("{{Zoom In}}"',
    'action("{{Zoom Out}}"',
    'action("{{Reset Zoom}}"',
    'action("{{Toggle Left Dock}}"',
    'action("{{Toggle Right Dock}}"',
    'action("{{Toggle Bottom Dock}}"',
    'action("{{Close All Docks}}"',
    'action("{{Split Up}}"',
    'action("{{Split Down}}"',
    'action("{{Split Left}}"',
    'action("{{Split Right}}"',
    'action("{{Project Panel}}"',
    'action("{{Outline Panel}}"',
    'action("{{Collab Panel}}"',
    'action("{{Terminal Panel}}"',
    'action("{{Diagnostics}}"',
    'action("{{Back}}"',
    'action("{{Forward}}"',
    'action("{{Command Palette...}}"',
    'action("{{Go to File...}}"',
    'action("{{Go to Symbol in Project}}"',
    'action("{{Go to Symbol in Editor...}}"',
    'action("{{Go to Line/Column...}}"',
    'action("{{Go to Definition}}"',
    'action("{{Go to Type Definition}}"',
    'action("{{Find All References}}"',
    'action("{{Next Problem}}"',
    'action("{{Previous Problem}}"',
    'action("{{Minimize}}"',
    'action("{{Zoom}}"',
    'action("{{View Telemetry}}"',
    'action("{{View Dependency Licenses}}"',
    'action("{{Show Welcome}}"',
    'action("{{Give Feedback...}}"',
    'action(\n                    "{{Open Recent...}}"',
    'action(\n                    "{{Close Editor}}"',
    'action(\n                    "{{Toggle Line Comment}}"',
    'action(\n                    "{{Select All}}"',
    'action(\n                    "{{Select Next Occurrence}}"',
    'action(\n                    "{{Documentation}}"',
    'action(\n                    "{{Zed Twitter}}"',
    'action(\n                    "{{Join the Team}}"',
]
replace_in_file(file_path, translation)

file_path = 'crates/zed/src/zed/open_listener.rs'
translation = [
    'format!("{{zed (pid {}) connected!}}"',
    'format!("{{error opening {:?}: {}}}"',
    'format!(\n                                                    "{{error opening {:?}: {}}}"',
]
replace_in_file(file_path, translation)

# ================================= regex end ================================


# 应用补丁
# apply patch
print(f'switch to dir: {BASE_PATH}')
os.chdir(BASE_PATH)
# os.system('npm install webpack --save-dev')
# os.system('npm run webpack')


print('=====================================')
if missing_files:
    print('missing_files! \n')
    for x in missing_files:
        print(x)
else:
    print('no missing file, good!')
print('=====================================')
unused_translations = [key for key in translation_dict if key and key not in used_translations]
if unused_translations:
    print('unused_translations! \n')
    for x in unused_translations:
        print(x)
else:
    print('no unused translation, good!')
print('=====================================')
if missing_translations:
    print('missing_translations! \n')
    for x in missing_translations:
        print(x)
else:
    print('no missing translation, good!')
print('=====================================')

print('finished!')
