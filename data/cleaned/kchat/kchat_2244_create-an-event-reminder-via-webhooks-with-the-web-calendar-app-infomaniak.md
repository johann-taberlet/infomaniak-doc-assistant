# Create an event reminder via webhooks with the Web Calendar app Infomaniak

Source: https://www.infomaniak.com/en/support/faq/2244/create-an-event-reminder-via-webhooks-with-the-web-calendar-app-infomaniak

---

This guide explains how to get event reminders from the Infomaniak Web app **Calendar** (online service [ksuite.infomaniak.com/calendar](https://ksuite.infomaniak.com/calendar)) on a chat system like [k Chat](https://infomaniak.com/gtl/kchat) or Slack.

**⚠ Available with:**

**limited to 1 webhook*

### Preamble

- This feature will allow you to be **notified in the chat of your choice** when an event is approaching.
- The **webhook** system is a method for an application or service to send information to another application or service in real-time, securely, and authenticated.

## Announce the webhook to Calendar

To add the webhook from your chat system to Calendar:

1. [Click here](https://ksuite.infomaniak.com/calendar)to access the Infomaniak Web app **Calendar** (online service [ksuite.infomaniak.com/calendar](https://ksuite.infomaniak.com/calendar)).
2. Click on the **Settings** icon at the top right.
3. Click on **Integrations** in the left sidebar.
4. Click on the **Add a webhook** button:

![image](https://faq.storage5.infomaniak.com/c36290e77de80a0b5d0d2ccfad218693d8d738f8.png)

5. Define:

![image](https://faq.storage5.infomaniak.com/07c59894d7ada1f5ca1925f2b7e6a84096b678f9.png)
A name to easily identify the Webhook when you add reminders. The webhook URL (obtained from your chat system - examples are presented further down in the FAQ). The elements (automatically taken from your event and/or added manually here) and their arrangement in the message to be sent: Insert %subject% to include the event subject. Insert %date% to include the event date. Insert %description% to include the event description. Insert %location% to include the possible location of the event.
6. Click on **Add**.

## Create an event with a chat reminder

Now that Calendar is linked to your chat account, you can choose to be notified in a chat when you add a reminder to an event:

1. [Click here](https://ksuite.infomaniak.com/calendar) to access the Infomaniak **Calendar** Web app (online service [ksuite.infomaniak.com/calendar](https://ksuite.infomaniak.com/calendar)).
2. Click on the [Create](https://www.infomaniak.com/en/support/faq/956) button in the top left corner.
3. Click on **Event**:

![image](https://faq.storage5.infomaniak.com/04396a8c467fd0fa1ce00aa6cfc324562541f6a7.png)
You could also click on an existing event on the calendar to modify it.
4. Display the **additional fields**:

![image](https://faq.storage5.infomaniak.com/44d6ef5c60fdddd5bd15fb30b36c3af8e6bd0b44.png)

5. Click on **Add a reminder**to configure it:

![image](https://faq.storage5.infomaniak.com/68bcb8d4e0c3f3883d06809c43e36b9c6644c04d.png)

6. In the reminder type dropdown menu, **choose the configured webhook**.
7. **Save the event at the bottom of the page.**

You will now receive a reminder in the chat corresponding to the webhook.

## Examples for obtaining a webhook

### k Chat

1. [Click here](https://ksuite.infomaniak.com/kchat) to access the **k Chat Web app** (online service [ksuite.infomaniak.com/kchat](https://ksuite.infomaniak.com/kchat)) or open the **k Chat desktop app** (desktop application on macOS / Windows / Linux).
2. Go to the [Integrations](https://www.infomaniak.com/en/support/faq/2001) section.
3. Click on **Incoming Webhooks**:

![image](https://faq.storage5.infomaniak.com/bf26b1aac8dfc5ffb27c08410ceccf400ac1928c.png)

4. Click on **Add** in the top right corner.
5. **Complete the required information** to create the "bot" that will post follow-up messages in k Chat in the channel of your choice:

![image](https://faq.storage5.infomaniak.com/2b558b3c60433e4fac3c544d28d36f9706a4f59b.png)

6. Save to obtain the webhook URL:

![image](https://faq.storage5.infomaniak.com/7689df2366aecfcf49273c6631d878eedf165719.png)

7. Create the custom notification in **Calendar** (read above if necessary):

![image](https://faq.storage5.infomaniak.com/8a0cd7210e52e4d9da08407cc996f887a6abe763.png)

8. Select your custom notification when adding a reminder to your event:

![image](https://faq.storage5.infomaniak.com/aac7afa7c82e00c4817c28eadefb245be4a4ea03.png)

### Slack

1. [Click here](https://slack.com/apps/new/A0F7XDUAZ-webhooks-entrants) to access Slack Web Hooks.
2. Choose the discussion thread where your reminders will appear (for example **@slackbot** or **#general**):

![image](https://faq.storage5.infomaniak.com/f67490b579ff0d247dd39159be5c9e4b71331f4e.png)

3. Save to get the webhook URL.

Create other webhooks to set reminders in other discussion threads.

#### Customize Slack reminder follow-ups

You can freely use [Slack formatting options](https://get.slack.help/hc/fr-fr/articles/202288908-Mettre-en-forme-vos-messages) in your notifications. Example in French:

```
N'oubliez pas de %subject% pour le %date%.
À prendre avec le jour J : %description%.
Lieu de l'évènement : %location%
```