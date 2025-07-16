import boto3
from botocore.exceptions import ClientError
import logging
import os
import requests
import json
from datetime import datetime

# Updated reports dictionary with shareholding pattern URLs
reports = {
    "2024-25": {
        "Jun 30th": "https://indianippon.com/wp-content/uploads/2024/07/shp_q1_2024-25.pdf",
        "Sept 30th": "https://indianippon.com/wp-content/uploads/2024/10/shp_q2_2024-25.pdf",
        "Dec 31st": "https://indianippon.com/wp-content/uploads/2025/01/shp_q3_2024_25.pdf",
        "Mar 31st": "https://indianippon.com/wp-content/uploads/2025/04/shp_31032025.pdf"
    },
    "2023-24": {
        "Jun 30th": "https://indianippon.com/wp-content/uploads/2023/07/shp-q1_2324.pdf",
        "Sept 30th": "https://indianippon.com/wp-content/uploads/2024/04/shp_q2_2023_24.pdf",
        "Dec 31st": "https://indianippon.com/wp-content/uploads/2024/01/shp_q3_2023_24.pdf",
        "Mar 31st": "https://indianippon.com/wp-content/uploads/2024/04/shp_q4_fy2023_24_final.pdf"
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
            # Add headers to mimic a browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            response = requests.get(url, headers=headers, allow_redirects=True, verify=False)
            
            if response.status_code == 200:
                # Check if the content is valid (not empty and is PDF)
                if response.content and response.headers.get('content-type', '').lower().startswith('application/pdf'):
                    self.s3_client.put_object(
                        Bucket=bucket_name,
                        Key=s3_key,
                        Body=response.content,
                        ContentType='application/pdf',
                        ACL='public-read'
                    )
                    return True, f"https://{bucket_name}.s3.ap-south-1.amazonaws.com/{s3_key}"
                else:
                    return False, "Invalid content or not a PDF file"
            return False, f"Failed to download from URL: {response.status_code}"
        except Exception as e:
            return False, str(e)

def generate_html_table(reports):
    """
    Generate HTML table for shareholding pattern with quarterly layout
    """
    html = """
    <html>
    <head>
        <style>
            table { 
                border-collapse: collapse; 
                width: 100%; 
                margin: 20px 0;
                font-family: Arial, sans-serif;
            }
            th, td { 
                border: 1px solid #ddd; 
                padding: 12px 8px; 
                text-align: center; 
            }
            th { 
                background-color: #f5f5f5;
                font-weight: bold;
            }
            .year-col {
                font-weight: bold;
                background-color: #f9f9f9;
            }
            a {
                color: #0066cc;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            h2 {
                font-family: Arial, sans-serif;
                color: #333;
                margin: 20px 0;
                text-align: center;
            }
            .quarter-header {
                background-color: #f0f0f0;
            }
        </style>
    </head>
    <body>
        <h2>QUARTER WISE DETAILS</h2>
        <table>
            <tr>
                <th rowspan="3">Financial<br>Year</th>
                <th colspan="4">QUARTER WISE DETAILS</th>
            </tr>
            <tr>
                <th>Q1</th>
                <th>Q2</th>
                <th>Q3</th>
                <th>Q4</th>
            </tr>
            <tr>
                <th>Quarter ended<br>Jun 30th</th>
                <th>Quarter ended<br>Sept 30th</th>
                <th>Quarter ended<br>Dec 31st</th>
                <th>Quarter ended<br>Mar 31st</th>
            </tr>
    """
    
    for year in sorted(reports.keys(), reverse=True):
        html += f"""
            <tr>
                <td class="year-col">{year}</td>
        """
        
        for quarter in ["Jun 30th", "Sept 30th", "Dec 31st", "Mar 31st"]:
            if quarter in reports[year]:
                url = reports[year][quarter]
                html += f'<td><a href="{url}" target="_blank">Download</a></td>'
            else:
                html += '<td>-</td>'
        
        html += '</tr>'
    
    html += """
        </table>
    </body>
    </html>
    """
    return html

def verify_url(url):
    """
    Verify if URL is accessible
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        response = requests.head(url, headers=headers, allow_redirects=True, verify=False, timeout=10)
        return response.status_code == 200
    except:
        return False

def generate_structured_json(reports):
    """
    Generate structured JSON for shareholding pattern reports
    """
    structured_data = {
        "title": "QUARTER WISE DETAILS",
        "type": "shareholding_pattern",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "years": []
    }

    for year in sorted(reports.keys(), reverse=True):
        year_data = {
            "financial_year": year,
            "quarters": {
                "Q1": {
                    "quarter_ended": "Jun 30th",
                    "download_url": reports[year].get("Jun 30th", None),
                    "s3_url": f"https://indian-nippon.s3.ap-south-1.amazonaws.com/investor/disclosure+under+reg46/ShareholdingPattern/{year}/{reports[year].get('Jun 30th', '').split('/')[-1]}" if reports[year].get("Jun 30th") else None
                },
                "Q2": {
                    "quarter_ended": "Sept 30th",
                    "download_url": reports[year].get("Sept 30th", None),
                    "s3_url": f"https://indian-nippon.s3.ap-south-1.amazonaws.com/investor/disclosure+under+reg46/ShareholdingPattern/{year}/{reports[year].get('Sept 30th', '').split('/')[-1]}" if reports[year].get("Sept 30th") else None
                },
                "Q3": {
                    "quarter_ended": "Dec 31st",
                    "download_url": reports[year].get("Dec 31st", None),
                    "s3_url": f"https://indian-nippon.s3.ap-south-1.amazonaws.com/investor/disclosure+under+reg46/ShareholdingPattern/{year}/{reports[year].get('Dec 31st', '').split('/')[-1]}" if reports[year].get("Dec 31st") else None
                },
                "Q4": {
                    "quarter_ended": "Mar 31st",
                    "download_url": reports[year].get("Mar 31st", None),
                    "s3_url": f"https://indian-nippon.s3.ap-south-1.amazonaws.com/investor/disclosure+under+reg46/ShareholdingPattern/{year}/{reports[year].get('Mar 31st', '').split('/')[-1]}" if reports[year].get("Mar 31st") else None
                }
            }
        }
        structured_data["years"].append(year_data)

    return structured_data

if __name__ == "__main__":
    # Disable SSL verification warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # AWS credentials and bucket configuration
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    BUCKET_NAME = 'indian-nippon'
    BASE_PATH = 'investor/disclosure under reg46/ShareholdingPattern'
    
    # Initialize S3 handler
    s3_handler = S3Handler(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    
    # Upload reports
    successful_uploads = {}
    for year, quarters in reports.items():
        successful_uploads[year] = {}
        for quarter, url in quarters.items():
            if url and verify_url(url):
                file_name = url.split('/')[-1]
                s3_key = f"{BASE_PATH}/{year}/{file_name}"
                
                success, result = s3_handler.upload_from_url(url, BUCKET_NAME, s3_key)
                if success:
                    print(f"Uploaded {year} {quarter} report: {result}")
                    successful_uploads[year][quarter] = url
                else:
                    print(f"Failed to upload {year} {quarter} report: {result}")
            else:
                print(f"Skipping {year} {quarter} - URL not accessible")
    
    # Generate and upload HTML table
    html_content = generate_html_table(reports)  # Use original reports to show all links
    
    # Generate structured JSON
    json_data = generate_structured_json(reports)
    
    try:
        # Upload HTML
        s3_handler.s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=f"{BASE_PATH}/index.html",
            Body=html_content,
            ContentType='text/html',
            ACL='public-read'
        )
        print(f"HTML table uploaded successfully: https://{BUCKET_NAME}.s3.ap-south-1.amazonaws.com/{BASE_PATH}/index.html")

        # Upload JSON
        s3_handler.s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=f"{BASE_PATH}/data.json",
            Body=json.dumps(json_data, indent=2),
            ContentType='application/json',
            ACL='public-read'
        )
        print(f"JSON data uploaded successfully: https://{BUCKET_NAME}.s3.ap-south-1.amazonaws.com/{BASE_PATH}/data.json")

        # Save local copy of JSON
        with open('shareholding_pattern_data.json', 'w') as f:
            json.dump(json_data, f, indent=2)
        print("Local JSON file saved as shareholding_pattern_data.json")

    except Exception as e:
        print(f"Failed to upload files: {str(e)}") 