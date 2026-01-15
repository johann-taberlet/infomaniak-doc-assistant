# Using kChat slash commands

Source: https://www.infomaniak.com/en/support/faq/2134/using-kchat-slash-commands

---

This guide covers messages that start with `/` on [kChat](https://infomaniak.com/gtl/kchat) interpreted as slash commands.

## Execute a slash command on kChat

To access slash commands on kChat:

1. Click in the composition field within a channel.
2. Enter a `/` (*slash* or *forward slash*) and the attached command.
3. Confirm to send the command.

If you type only the `/` sign, a modal appears with the commands that can be executed, such as going offline, for example.

Here is a table of the main commands:

## Create a custom slash command

### Prerequisites

- Not be an external user (they will not see the menu *Integrations*).

To create a **custom slash command**:

1. [Click here‍](https://kchat.infomaniak.com/)to access the **Web kChat** app (online service [kchat.infomaniak.com](https://kchat.infomaniak.com/)) or open the **desktop kChat** app (desktop application on macOS / Windows / Linux).
2. Click on the **New** icon ‍ next to your kChat organization name.
3. Click on **Integrations**: 

![image](https://faq.storage5.infomaniak.com/e205799c5c7e403b92ae0dd1921f78bfd456087a.png)

4. Click on **Slash command**: 

![image](https://faq.storage5.infomaniak.com/07c786ce8bbc87e358d111d1e40759b51cb1b8c2.png)

5. Click the blue button to **Add a command**: 

![image](https://faq.storage5.infomaniak.com/e05ee003cd93e6c0f2f81f4e09de5c048088412e.png)

6. Configure the slash command (name, trigger (without the `/`), expected content type, action to execute*, etc., including whether the command should appear in the help modal mentioned in the chapter above).* This can include calling an external API, running a script, displaying a specific response, etc. For this, you will generally need an external script or application that will respond to the commands. You can also set additional parameters for the command, such as dropdown options, checkboxes, etc., depending on your needs.
7. **Save** the command.
8. Make sure to test the command to ensure it works as expected.

> **Note:** Remember that creating custom slash commands may require additional programming skills, especially if you need to integrate custom features or interactions with external systems. Also, make sure to follow security best practices when creating these commands to avoid potential security vulnerabilities.