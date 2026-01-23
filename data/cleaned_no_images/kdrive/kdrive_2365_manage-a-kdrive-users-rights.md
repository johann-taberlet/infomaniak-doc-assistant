# Manage a k Drive user's rights

Source: https://www.infomaniak.com/en/support/faq/2365/manage-a-kdrive-users-rights

---

This guide explains how user permissions work on [k Drive](https://infomaniak.com/gtl/kdrive) and how you can modify these access permissions.

## How k Drive user permissions work

You can add a new user to k Drive (*k Drive Pro* for example, therefore outside *k Suite*), and define 2 levels of permissions, via **folder sharing**…

… or via **k Drive user management**:

In both cases, **2 levels of permissions** are offered:

1. **Administrator** gives users the same rights as the k Drive owner: Sharing, statistics, activity reports, restoring and deleting folders, importing external data, etc. and accessing files and folders…
2. **User** allows access to folders located at the root of the k Drive as well as managing and freely sharing their content: Access to shared files and folders, personal directory and file creation/sharing…However, users will not be able to access the administrative management of the product (manage users, view statistics, create or delete folders at the root of the k Drive, import data from an external service, etc.)…

In all cases:

- The content of the **Organization Folders** directory is common and visible to other k Drive users, but sharing [can be restricted](https://www.infomaniak.com/en/support/faq/2501).
- Contents shared by other users from their private part of the k Drive are not listed in the **Shares** menu of other users.
- Any folder or file [can be shared with other k Drive users](https://www.infomaniak.com/en/support/faq/2382) and the contacts of your choice.

## Modify a k Drive user's permissions

To access k Drive and manage user rights:

1. [Click here](https://ksuite.infomaniak.com/kdrive) to access the Infomaniak **k Drive** Web app (online service [ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive)).
2. Check or select the relevant k Drive in the dropdown menu of the left sidebar.
3. Click on **the action menu ⋮** located to the right of the relevant item.
4. Click on **Manage users**:

5. Manage the desired user's rights, choose the desired access level:

### In case of a problem

If a modification is not possible:

… then you need to act on the user's rights **at the Organization level itself**:

… and reduce their role **as an administrator** by giving them a **user** role:

Thus, the proposed modification in point 5 above will now be accessible:

### Other actions on the user

If necessary, open the action menu **⋮** of the desired user for **advanced actions**:

You can manage the user, view their activity, block their access, and completely remove them from k Drive.

If necessary, also manage the permissions related to actions on [categories](https://www.infomaniak.com/en/support/faq/2628):

## Rights in the Organization / Rights on k Drive

As seen above, do not confuse or mix:

- the rights granted for the **management of the k Drive service on the Manager**,
- and the rights granted to the user **within k Drive**.

Indeed, a user may have **restricted or no rights** on the k Drive product in the Manager (they will therefore not have the ability to manage the k Drive product themselves or have technical details - see below) but may have been defined as an **administrator** in k Drive and thus have access to all stored data.

### Rights in the Organization: product management

In this example, you can manage the k Drive management rights of the user `ralph` from the product accesses:

If necessary, specify which k Drive is concerned and especially which permissions (**technical** / **statistics**) they should have:

With only **Technical** rights, they will not see the **Statistics** element in the sidebar:

If, on the other hand, only the **Statistics** box is activated, then they will not access the **dashboard**:

And if the administrator deactivates both **Technical** and **Statistics** boxes, only the storage information is accessible from the sidebar:

### User rights on k Drive

Even with both **Technical** and **Statistics** boxes (mentioned above) activated, a user who only has **User** rights at the level of k Drive user management will not be able to, among other things, create a new folder at the root of the **Organization Folders**:

The user will need an **Administrator** role (see point 5 above) to access this window for creating a new **Organization Folder** at the root: