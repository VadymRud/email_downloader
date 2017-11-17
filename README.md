From the "Initial spec" issue:

---

The library should consist of a single class, that is used as follows:

```python
mailbox = EmailLib(hostname="some.hostname.com", ssl=True, port=993, email="some_email@some.hostname.com", password="some_password")

mailbox.checksize()  # This should return the size in MB i.e. "1267.5" (~1.3G); this can be achieved by checking the sizes of all e-mail messages, from all folders, and adding them together.

mailbox.downloadmails(dir="/home/user/dl_dir")  # This should download all e-mail messages, from all folders, into the local directory specified, or use the current working directory as a default. It should preserve the e-mail account's folder structure, i.e. "Sent" -> "Sent", "Drafts -> "Drafts", "Inbox" -> "Inbox", etc.

mailbox.uploadmails(dir="/home/user/dl_dir", hostname="other.hostname.com", ssl=True, port=993, email="other_email@other.hostname.com", password="some_other_password")  # This should upload all e-mail messages, from all folders, from the local directory specified, or use the current working directory as a default. It should preserve the e-mail account's folder structure, i.e. "Sent" -> "Sent", "Drafts -> "Drafts", "Inbox" -> "Inbox", etc.

mailbox.transfermails(dir="/home/user/dl_dir", hostname="other.hostname.com", ssl=True, port=993, email="other_email@other.hostname.com", password="some_other_password")  # This should simply perform mailbox.downloadmails() and then mailbox.uploadmails(), as a convenience function.

```

The tasks may have to be implemented asynchronously, or at least have the option to be, as we may have to download 1,000s or 10,000s of e-mail messages, which has the potential of being a very slow operation.