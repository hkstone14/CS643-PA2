## CS643-PA2

### Link For GitHub
https://github.com/hkstone14/CS643-PA2

### Link For Docker Hub
https://hub.docker.com/r/hkstone14/harikrushna-patel-cs643

### Setup EMR Cluster
<ol>
<li>Navigate to Amazon EMR: https://console.aws.amazon.com/elasticmapreduce/home?region=us-east-1</li>
<li>Create Cluster</li>
<li>Click On Advanced Options and Select 'Spark 2.4.7' and then click Next</li>
<li>
Use the following configuration: <br/>
1. Uniform instance groups. <br/>
2. Select an instance type, these MUST be the same for the master, core, and task. I tested with m4.xlarge, and would
recommend anything above m4.xlarge. <br/>
3. Ensure you have 1 master, 2 cores, and 1 task <br/>
4. Check Cluster Scaling, and enable 'Use EMR-managed scaling', and then click Next. <br/>
5. Click Next only if default configurations are required. <br/>
6. Select your keypair, if no key pairs, then create one and select the following roles for instance profile and EMR role:
EC2 instance profile:EMR_EC2_DefaultRole
EMR role:EMR_DefaultRole <br/>
7. Create Cluster <br/>
8. While your cluster is being provisioned, go to the EC2 dashboard, and ensure you have both the ElasticMapReduce-master and ElasticMapReduce-slave up and running. <br/>
9. Once it's running, navigate back into the EMR dashboard, and ensure the security groups for Master has SSH enabled, if not enabled, please enable it on Port 22. <br/>
10. Log into the master node as the following ssh -i KEYPAIR hadoop@ip_address_for_emr_node <br/>
</li>
</ol>

### Setup S3 Bucket
<ol>
<li>Create an S3 Bucket</li>
<li>Load in your csv files for the training dataset, and the validation dataset</li>
</ol>

### Running ML Model
<ol>
<li>After your logged into the master node, from the previous configuration steps, install both docker and git by the running the following:
<ol>
<li>
sudo yum install docker -y
</li>
<li>
sudo yum install git -y
</li>
</ol></li>
<li>Load the files for project, either by performing git clone or scp into the machine as follows:
<ol>
<li>
GIT: git clone https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git <br/>
</li>
<li>
SCP: scp -r . -i YOUR_KEY_PAIR.pem hadoop@ip_address_for_emr_node
</li>
</ol>
</li>
<li>
Since we will be using spark-submit, please copy your csv files into the following directory
user/hadoop. <br/>
NOTE: This is only for local files that want to be read, we will see later how to fetch from an S3 Bucket.
Run the following command: sudo hdfs dfs -copyFromLocal *.csv /user/hadoop
</li>
<li>
To run train.py issue the following commands:
sudo spark-submit train.py ARGUMENTS_FOR_CSV_FILE OR
sudo python3 train.py ARGUMENTS_FOR_CSV_FILE [only for local]
By default, we will be using TrainingDataset.csv if no arguments are given.
This will generate an F1 Score.
If you want to read from an S3 Bucket: use the following arguments
s3://YOUR_BUCKET_NAME/NAME_OF_DATASET.csv
</li>
<li>
To run prediction.py issue the following commands:
<ul>
    <li>
         With Docker: <br/>
            docker build --tag NAME_OF_YOUR_IMAGE . --no-cache <br/>
            docker run NAME_OF_YOUR_IMAGE ARGUMENTS_FOR_DATASET
            Ex: docker run NAME_OF_YOUR_IMAGE ValidationDataset.csv
    </li>
    <li>
         Without Docker: <br/>
            sudo spark-submit prediction.py ARGUMENTS_FOR_CSV_FILE. By default, we will be using ValidationDataset.csv if no arguments are given
            sudo python3 prediction.py ARGUMENTS_FOR_CSV_FILE [only for local]
    </li>
</ul>
</li>
</ol>