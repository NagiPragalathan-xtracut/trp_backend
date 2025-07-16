import boto3
from botocore.exceptions import ClientError
import logging
import os
import requests
from datetime import datetime


reports = {
    "2024-25": {
        "Jun 30th": "https://indianippon.com/wp-content/uploads/2024/07/cg_q1_2024-25.pdf",
        "Sept 30th": "https://indianippon.com/wp-content/uploads/2024/10/cg_q2_2024-25.pdf",
        "Dec 31st": "https://indianippon.com/wp-content/uploads/2025/01/cg_q3_2024_25.pdf",
        "Mar 31st": "https://indianippon.com/wp-content/uploads/2025/05/ifg31032025.pdf"
    },
    "2023-24": {
        "Jun 30th": "https://indianippon.com/wp-content/uploads/2023/07/cgr-q1_2324.pdf",
        "Sept 30th": "https://indianippon.com/wp-content/uploads/2023/10/cgi_q2_2023_24.pdf",
        "Dec 31st": "https://indianippon.com/wp-content/uploads/2024/01/cg_q3_2023_24.pdf",
        "Mar 31st": "https://indianippon.com/wp-content/uploads/2024/04/cg_q4_2023_24_final.pdf"
    },
    "2022-23": {
        "Jun 30th": "https://indianippon.com/wp-content/uploads/2022/07/cgr_q1_2223.pdf",
        "Sept 30th": "https://indianippon.com/wp-content/uploads/2022/10/cgr_q2_2223.pdf",
        "Dec 31st": "https://indianippon.com/wp-content/uploads/2023/01/cgr_q3_2223.pdf",
        "Mar 31st": "https://indianippon.com/wp-content/uploads/2023/04/cgr_q4_22_23.pdf"
    },
    "2021-22": {
        "Jun 30th": "https://indianippon.com/wp-content/uploads/2021/07/cgr_q1_2122.pdf",
        "Sept 30th": "https://indianippon.com/wp-content/uploads/2021/10/cgr_q2_2122.pdf",
        "Dec 31st": "https://indianippon.com/wp-content/uploads/2022/01/cgr_q3_2122.pdf",
        "Mar 31st": "https://indianippon.com/wp-content/uploads/2022/04/cgr_q4_2122.pdf"
    },
    "2020-21": {
        "Jun 30th": "http://indianippon.com/wp-content/uploads/2020/07/cgr_30062020.pdf",
        "Sept 30th": "http://indianippon.com/wp-content/uploads/2020/10/cg_report_q2_2020_21.pdf",
        "Dec 31st": "http://indianippon.com/wp-content/uploads/2021/02/cgr_q3_2020-21.pdf",
        "Mar 31st": "https://indianippon.com/wp-content/uploads/2021/04/cgr_q4_2020-21.pdf"
    },
    "2019-20": {
        "Jun 30th": "http://indianippon.com/wp-content/uploads/2019/07/cg_30062019120719.pdf",
        "Sept 30th": "http://indianippon.com/wp-content/uploads/2019/10/cg_30092019_final.pdf",
        "Dec 31st": "http://indianippon.com/wp-content/uploads/2020/01/cg_31122019.pdf",
        "Mar 31st": "http://indianippon.com/wp-content/uploads/2020/05/cg_31032020.pdf"
    },
    "2018-19": {
        "Jun 30th": "http://indianippon.com/wp-content/uploads/2018/07/cg_30th_june_2018.pdf",
        "Sept 30th": "http://indianippon.com/wp-content/uploads/2018/10/cg_report-q2-2018-19.pdf",
        "Dec 31st": "http://indianippon.com/wp-content/uploads/2019/01/cg_report_htmlformat.pdf",
        "Mar 31st": "http://indianippon.com/wp-content/uploads/2019/04/corporategovernance_31032019.pdf"
    },
    "2017-18": {
        "Jun 30th": "http://indianippon.com/result/CG_30TH_JUNE_2017.pdf",
        "Sept 30th": "http://indianippon.com/result/CG_30TH_SEPTEMBER_2017.pdf",
        "Dec 31st": "http://indianippon.com/wp-content/uploads/2018/01/CG_31ST_DECEMBER_2017.pdf",
        "Mar 31st": "http://indianippon.com/wp-content/uploads/2018/04/CG_31ST_MARCH_2018.pdf"
    },
    "2016-17": {
        "Jun 30th": "http://indianippon.com/result/CG_30TH_JUNE_2016.pdf",
        "Sept 30th": "http://indianippon.com/result/CG_30TH_SEPTEMBER_2016.pdf",
        "Dec 31st": "http://indianippon.com/result/CG_31ST_DECEMBER_2016.pdf",
        "Mar 31st": "http://indianippon.com/result/CG_31ST_MARCH_2017.pdf"
    },
    "2015-16": {
        "Jun 30th": "http://indianippon.com/result/CG_30TH_JUNE_2015.pdf",
        "Sept 30th": "http://indianippon.com/result/CG_30TH_SEPTEMBER_2015.pdf",
        "Dec 31st": "http://indianippon.com/result/CG_31ST_DECEMBER_2015.pdf",
        "Mar 31st": "http://indianippon.com/result/CG_31ST_MARCH_2016.pdf"
    },
    "2014-15": {
        "Jun 30th": "http://indianippon.com/result/CG_30TH_JUNE_2014.PDF",
        "Sept 30th": "http://indianippon.com/result/CG_30TH_SEPTEMBER_2014.pdf",
        "Dec 31st": "http://indianippon.com/result/CG_31ST_DECEMBER_2014.pdf",
        "Mar 31st": "http://indianippon.com/result/CG_31ST_MARCH_2015.pdf"
    },
    "2013-14": {
        "Jun 30th": "http://indianippon.com/result/CG_30TH_JUNE_2013.pdf",
        "Sept 30th": "http://indianippon.com/result/CG_30TH_SEPTEMBER_2013.pdf",
        "Dec 31st": "http://indianippon.com/result/CG_31ST_DECEMBER_2013.pdf",
        "Mar 31st": "http://indianippon.com/result/CG_31ST_MARCH_2014.pdf"
    },
    "2012-13": {
        "Jun 30th": "http://indianippon.com/result/CG_30TH_JUNE_2014.pdf",
        "Sept 30th": "http://indianippon.com/result/CG_30TH_SEPTEMBER_2014.pdf",
        "Dec 31st": "http://indianippon.com/result/CG_31ST_DECEMBER_2014.pdf",
        "Mar 31st": "http://indianippon.com/result/CG_31ST_MARCH_2013.pdf"
    },
    "2011-12": {
        "Jun 30th": "http://indianippon.com/result/CG_30TH_JUNE_2013.pdf",
        "Sept 30th": "http://indianippon.com/result/CG_30TH_SEPTEMBER_2013.pdf",
        "Dec 31st": "http://indianippon.com/result/CG_31ST_DECEMBER_2013.pdf",
        "Mar 31st": "http://indianippon.com/result/CG_31ST_MARCH_2012.pdf"
    },
    "2010-11": {
        "Jun 30th": "http://indianippon.com/result/CG_30TH_JUNE_2012.pdf",
        "Sept 30th": "http://indianippon.com/result/CG_30TH_SEPTEMBER_2012.pdf",
        "Dec 31st": "http://indianippon.com/result/CG_31ST_DECEMBER_2012.pdf",
        "Mar 31st": "http://indianippon.com/result/CG_31ST_MARCH_2011.pdf"
    }
}


class S3Handler:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name='ap-south-1'):
        """
        Initialize S3 client with AWS credentials
        """
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def upload_from_url(self, url, bucket_name, s3_key):
        """
        Download file from URL and upload to S3
        """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.s3_client.put_object(
                    Bucket=bucket_name,
                    Key=s3_key,
                    Body=response.content,
                    ACL='public-read'
                )
                return True, f"https://{bucket_name}.s3.ap-south-1.amazonaws.com/{s3_key}"
            return False, f"Failed to download from URL: {response.status_code}"
        except Exception as e:
            return False, str(e)

def generate_html_table(reports):
    """
    Generate HTML table for shareholding pattern
    """
    html = """
    <html>
    <head>
        <style>
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid black; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h2>Shareholding Pattern Reports</h2>
        <table>
            <tr>
                <th>Year</th>
                <th>Quarter</th>
                <th>Report Link</th>
            </tr>
    """
    
    for year in sorted(reports.keys(), reverse=True):
        for quarter in ["Jun 30th", "Sept 30th", "Dec 31st", "Mar 31st"]:
            if quarter in reports[year]:
                file_name = reports[year][quarter].split('/')[-1]
                html += f"""
                <tr>
                    <td>{year}</td>
                    <td>{quarter}</td>
                    <td><a href="https://indian-nippon.s3.ap-south-1.amazonaws.com/investor/disclosure+under+reg46/ShareholdingPattern/{year}/{file_name}" target="_blank">View Report</a></td>
                </tr>
                """
    
    html += """
        </table>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    # AWS credentials and bucket configuration
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    BUCKET_NAME = 'indian-nippon'
    BASE_PATH = 'investor/disclosure under reg46/ShareholdingPattern'
    
    # Initialize S3 handler
    s3_handler = S3Handler(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    
    # Upload reports
    for year, quarters in reports.items():
        for quarter, url in quarters.items():
            if url:
                file_name = url.split('/')[-1]
                s3_key = f"{BASE_PATH}/{year}/{file_name}"
                
                success, result = s3_handler.upload_from_url(url, BUCKET_NAME, s3_key)
                if success:
                    print(f"Uploaded {year} {quarter} report: {result}")
                else:
                    print(f"Failed to upload {year} {quarter} report: {result}")
    
    # Generate and upload HTML table
    html_content = generate_html_table(reports)
    try:
        s3_handler.s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=f"{BASE_PATH}/index.html",
            Body=html_content,
            ContentType='text/html',
            ACL='public-read'
        )
        print(f"HTML table uploaded successfully: https://{BUCKET_NAME}.s3.ap-south-1.amazonaws.com/{BASE_PATH}/index.html")
    except Exception as e:
        print(f"Failed to upload HTML table: {str(e)}")

