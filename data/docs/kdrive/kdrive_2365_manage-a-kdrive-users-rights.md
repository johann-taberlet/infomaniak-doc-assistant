# Manage a kDrive user's rights

Source: https://www.infomaniak.com/en/support/faq/2365/manage-a-kdrive-users-rights

---

This guide explains how user permissions work on [kDrive](https://infomaniak.com/gtl/kdrive) and how you can modify these access permissions.

## How kDrive user permissions work

You can add a new user to kDrive (*kDrive Pro* for example, therefore outside *kSuite*), and define 2 levels of permissions, via **folder sharing**…

![image](https://faq.storage5.infomaniak.com/883df6c7622d962c1c65c6a56e7cd8fd42c2ca87.png)

![image](https://faq.storage5.infomaniak.com/fa610afd5f8f63d2c93ab889281f868c6cc3d870.png)

… or via **kDrive user management**:

![image](https://faq.storage5.infomaniak.com/cd8284033dfa6513fc372392c0f9cd18a38f4507.png)

![image](https://faq.storage5.infomaniak.com/ffb1050fecc333562fad48baa283abdde41ab9b1.png)

In both cases, **2 levels of permissions** are offered:

1. **Administrator** gives users the same rights as the kDrive owner:Sharing, statistics, activity reports, restoring and deleting folders, importing external data, etc. and accessing files and folders…
2. **User** allows access to folders located at the root of the kDrive as well as managing and freely sharing their content:Access to shared files and folders, personal directory and file creation/sharing…However, users will not be able to access the administrative management of the product (manage users, view statistics, create or delete folders at the root of the kDrive, import data from an external service, etc.)…

In all cases:

- The content of the **Organization Folders** directory is common and visible to other kDrive users, but sharing [can be restricted](https://www.infomaniak.com/en/support/faq/2501).
- Contents shared by other users from their private part of the kDrive are not listed in the **Shares** menu of other users.
- Any folder or file [can be shared with other kDrive users](https://www.infomaniak.com/en/support/faq/2382) and the contacts of your choice.

## Modify a kDrive user's permissions

To access kDrive and manage user rights:

1. [Click here](https://ksuite.infomaniak.com/kdrive) to access the Infomaniak **kDrive** Web app (online service [ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive)).
2. Check or select the relevant kDrive in the dropdown menu of the left sidebar.
3. Click on **the action menu ⋮** located to the right of the relevant item.
4. Click on **Manage users**:

![image](https://faq.storage5.infomaniak.com/b96e904458f2104485cd96ed8f16ffd204d933a8.png)

5. Manage the desired user's rights, choose the desired access level:

![image](https://faq.storage5.infomaniak.com/ba5837cd72f2264699ae14e61d33d289a7feee24.png)

 

### In case of a problem

If a modification is not possible:

![image](https://faq.storage5.infomaniak.com/bb302de35d2954e1ce301eae95b3cff83f3aba3c.png)

… then you need to act on the user's rights **at the Organization level itself**:

![image](https://faq.storage5.infomaniak.com/adccaf34ecd6433ab9841ae97329e8ea8549b701.png)

… and reduce their role **as an administrator** by giving them a **user** role:

![image](https://faq.storage5.infomaniak.com/6511be5da985fa19a4dc31c5ac0cc18de45b2587.png)

Thus, the proposed modification in point 5 above will now be accessible:

![image](https://faq.storage5.infomaniak.com/c183fabe6d2317e969875901a4c57921409e69e3.png)

### Other actions on the user

If necessary, open the action menu **⋮** of the desired user for **advanced actions**:

![image](https://faq.storage5.infomaniak.com/f22408c288fd937c388214feba51d5395ba07152.png)

You can manage the user, view their activity, block their access, and completely remove them from kDrive.

If necessary, also manage the permissions related to actions on [categories](https://www.infomaniak.com/en/support/faq/2628):

![image](https://faq.storage5.infomaniak.com/f2f2ac389724ef7bac8e32cd8060e13fbdb1cafa.png)

## Rights in the Organization / Rights on kDrive

As seen above, do not confuse or mix:

- the rights granted for the **management of the kDrive service on the Manager**,
- and the rights granted to the user **within kDrive**.

Indeed, a user may have **restricted or no rights** on the kDrive product in the Manager (they will therefore not have the ability to manage the kDrive product themselves or have technical details - see below) but may have been defined as an **administrator** in kDrive and thus have access to all stored data.

### Rights in the Organization: product management

In this example, you can manage the kDrive management rights of the user `ralph` from the product accesses:

![image](https://faq.storage5.infomaniak.com/1e0d8aa41aa0c44a6d72c85672d9375641f2b086.png)

If necessary, specify which kDrive is concerned and especially which permissions (**technical** / **statistics**) they should have:

![image](https://faq.storage5.infomaniak.com/29222ce90a057a6bc74b9a5d18adf4602cb02ba6.png)

With only **Technical** rights, they will not see the **Statistics** element in the sidebar:

![image](https://faq.storage5.infomaniak.com/2c0d5e4ccd5fe46b42150a2d3790848f60e619e6.png)

If, on the other hand, only the **Statistics** box is activated, then they will not access the **dashboard**:

![image](https://faq.storage5.infomaniak.com/cf61dfd9778b8b82752f063056b6197a2cca3f80.png)

And if the administrator deactivates both **Technical** and **Statistics** boxes, only the storage information is accessible from the sidebar:

![image](https://faq.storage5.infomaniak.com/56d8872f5720cee5139af412a6285a6db44b76e9.png)

### User rights on kDrive

Even with both **Technical** and **Statistics** boxes (mentioned above) activated, a user who only has **User** rights at the level of kDrive user management will not be able to, among other things, create a new folder at the root of the **Organization Folders**:

![image](https://faq.storage5.infomaniak.com/60aa4b4526d76de9f53a2da313d3684952a0f86a.png)

The user will need an **Administrator** role (see point 5 above) to access this window for creating a new **Organization Folder** at the root:

![image](https://faq.storage5.infomaniak.com/ccac9df6d8d02e1cbbda2a0349339217ecce624f.png)