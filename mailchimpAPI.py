import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

# 配置 Mailchimp API
def configure_mailchimp(api_key, server):
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": api_key,
        "server": server
    })
    return client

# 創建 List
def create_list(mailchimp_client, list_data):
    try:
        response = mailchimp_client.lists.create_list(list_data)
        print("List created successfully:", response)
        return response["id"]
    except ApiClientError as error:
        print("An error occurred while creating list:", error.text)
        return None

# 添加成員到List
def add_member_to_list(mailchimp_client, list_id, email):
    try:
        response = mailchimp_client.lists.add_list_member(list_id, {
            "email_address": email,
            "status": "subscribed"
        })
        print(f"Member {email} added successfully:", response)
        return response
    except ApiClientError as error:
        print(f"An error occurred while adding {email} to the list:", error.text)
        return None

# 創建 Campaign
def create_campaign(mailchimp_client, list_id, campaign_data):
    try:
        campaign_data["recipients"]["list_id"] = list_id
        response = mailchimp_client.campaigns.create(campaign_data)
        print("Campaign created successfully:", response)
        return response["id"]
    except ApiClientError as error:
        print("An error occurred while creating campaign:", error.text)
        return None

# 發送 Campaign
def send_campaign(mailchimp_client, campaign_id):
    try:
        response = mailchimp_client.campaigns.send(campaign_id)
        print("Campaign sent successfully:", response)
    except ApiClientError as error:
        print("An error occurred while sending campaign:", error.text)

# 獲取 Campaign 信息
def get_campaign_info(mailchimp_client, campaign_id):
    try:
        response = mailchimp_client.campaigns.get(campaign_id)
        print("Campaign info:", response)
        return response
    except ApiClientError as error:
        print("An error occurred while fetching campaign info:", error.text)
        return None

# 主函數
def main():
    api_key = "f068548ad120f1f67a3d070368772ba7-us19"
    server = "us19"
    mailchimp = configure_mailchimp(api_key, server)

    # 創建list
    list_data = {
        "permission_reminder": "You signed up for updates on our website",
        "email_type_option": False,
        "campaign_defaults": {
            "from_name": "Your Name",
            "from_email": "your_email@example.com",
            "subject": "Test Campaign",
            "language": "EN_US"
        },
        "name": "Test List",
        "contact": {
            "company": "Your Company",
            "address1": "123 Main St",
            "city": "Anytown",
            "state": "NY",
            "zip": "12345",
            "country": "US"
        }
    }

    # 創建List
    list_id = create_list(mailchimp, list_data)
    if not list_id:
        return

    # 添加成員到List
    add_member_to_list(mailchimp, list_id, "choutwn@gmail.com")
    add_member_to_list(mailchimp, list_id, "luohsuan.ho@ematicsolutions.com")

    # 創建campaign
    campaign_data = {
        "type": "regular",
        "recipients": {},
        "settings": {
            "subject_line": "Hello from Mailchimp",
            "preview_text": "This is a test campaign",
            "title": "Test Campaign Title",
            "from_name": "Your Name",
            "reply_to": "your_email@example.com",
            "to_name": "Subscriber"
        }
    }
    campaign_id = create_campaign(mailchimp, list_id, campaign_data)
    if not campaign_id:
        return

    # 發起campaign
    send_campaign(mailchimp, campaign_id)

    # 獲取campaign訊息並打印
    get_campaign_info(mailchimp, campaign_id)

if __name__ == "__main__":
    main()

