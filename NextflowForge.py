import streamlit as st


# Helper functions to generate content for the Nextflow file
def generate_nextflow_file(
    project_info, parameters, processes, environment, output_config, scheduler
):
    """
    Generates the content of a Nextflow configuration file or script based on the collected inputs.

    :param project_info: Dictionary containing project information (name, description, author).
    :param parameters: List of dictionaries, each containing parameter details.
    :param processes: List of dictionaries, each representing a Nextflow process.
    :param environment: Dictionary containing environment setup details (Docker, Singularity, etc.).
    :param output_config: Dictionary with output configuration settings.
    :param scheduler: Dictionary with cluster or cloud scheduler settings.

    :return: String representing the content of the Nextflow file.
    """
    # Initialize the content with project information
    content = f"// Nextflow Workflow - {project_info['name']}\n"
    content += f"// Description: {project_info['description']}\n"
    content += (
        f"// Author: {project_info['author_name']} ({project_info['author_email']})\n\n"
    )

    # Include workflow parameters
    if parameters:
        content += "params {\n"
        for param in parameters:
            param_line = f"  {param['name']} = "
            if param["type"] == "String":
                param_line += f"'{param['default']}'"
            else:
                param_line += f"{param['default']}"
            content += param_line + f" // {param['description']}\n"
        content += "}\n\n"

    # Include environment setup
    if environment["container"] == "Docker":
        content += f"process.container = '{environment['docker_image']}'\n\n"
    elif environment["container"] == "Conda" and environment["conda_file_name"]:
        content += f"process.conda = '{environment['conda_file_name']}'\n\n"

    # Output configuration
    if output_config:
        content += f"process.publishDir = '{output_config['output_dir']}'\n"
        if output_config["generate_logs"]:
            content += "process.debug = true\n"
        if output_config["file_naming"]:
            content += f"process.filePattern = '{output_config['file_naming']}'\n"
        content += "\n"

    # Define processes
    for process in processes:
        content += f"process {process['name']} {{\n"
        content += "  input:\n"
        content += f"    {process['input']}\n"
        content += "  output:\n"
        content += f"    {process['output']}\n"
        content += "  script:\n"
        content += f"    \"\"\"\n{process['command']}\n\"\"\"\n"
        content += "}\n\n"

    # Scheduler/Cluster settings
    if scheduler["scheduler"] != "None":
        content += "// Scheduler Settings\n"
        content += f"process.executor = '{scheduler['scheduler']}'\n"
        if scheduler["queue"]:
            content += f"process.queue = '{scheduler['queue']}'\n"
        content += "\n"

    return content


def collect_parameters():
    """
    Collect user-defined parameters for the Nextflow workflow.

    :return: List of parameter dictionaries.
    """
    parameters = []
    param_name = st.text_input("Parameter Name")
    param_type = st.selectbox(
        "Parameter Type", ["String", "Integer", "Boolean", "Float"]
    )
    param_default = st.text_input("Default Value")
    param_description = st.text_area("Parameter Description")

    if st.button("Add Parameter"):
        if param_name and param_default:
            parameters.append(
                {
                    "name": param_name,
                    "type": param_type,
                    "default": param_default,
                    "description": param_description,
                }
            )
            st.success(f"Parameter '{param_name}' added!")
    return parameters


def collect_processes():
    """
    Collect process definitions for the Nextflow workflow.

    :return: List of process dictionaries.
    """
    processes = []
    process_name = st.text_input("Process Name")
    command = st.text_area("Command to Run")
    input_files = st.text_area("Input Files Dependencies (e.g., file1 from input1)")
    output_files = st.text_area("Output Files Declarations (e.g., file1 into output1)")

    if st.button("Add Process"):
        if process_name and command:
            processes.append(
                {
                    "name": process_name,
                    "command": command,
                    "input": input_files,
                    "output": output_files,
                }
            )
            st.success(f"Process '{process_name}' added!")
    return processes


# Streamlit App
st.title("Nextflow Workflow Generator")

# Step 1: Workflow Information
st.markdown("### Step 1: Workflow Information")
st.markdown(
    """
    **What is this step?**  
    Here, you provide basic information about the workflow:
    
    - **Project Name**: A unique name for the workflow.  
    - **Description**: A brief description of the analysis or tasks the workflow will perform.  
    - **Author**: Information about the creator of the workflow.
    
    **Example**:  
    - Project Name: `RNA_Seq_Analysis`  
    - Description: `This workflow analyzes RNA-Seq data to identify differential gene expression between conditions.`  
    - Author: `Jane Doe`, `jane.doe@example.com`
    """
)
project_info = {
    "name": st.text_input("Project Name"),
    "description": st.text_area("Workflow Description"),
    "author_name": st.text_input("Author Name"),
    "author_email": st.text_input("Author Email"),
}

# Step 2: Input Files
st.markdown("### Step 2: Input Files")
st.markdown(
    """
    **What is this step?**  
    Here, you upload the files that will be used in your analysis:
    
    - **Primary Data Files**: These are the main datasets you'll be analyzing (e.g., FASTQ files for sequencing data).  
    - **Reference Files**: Files used as a reference (e.g., a genome reference in `.fa` format).  
    - **Config Files**: Additional configuration settings in a file.
    
    **Example**:  
    - Primary Data File: `sample_data.fastq`  
    - Reference File: `human_genome.fa`  
    - Config File: `workflow_settings.config`
    """
)
uploaded_data_files = st.file_uploader(
    "Upload Primary Data Files", accept_multiple_files=True
)
uploaded_reference_files = st.file_uploader(
    "Upload Reference Files", accept_multiple_files=True
)
uploaded_config_files = st.file_uploader(
    "Upload Additional Config Files", accept_multiple_files=True
)

# Step 3: Pipeline Parameters
st.markdown("### Step 3: Pipeline Parameters")
st.markdown(
    """
    **What is this step?**  
    This is where you define parameters that the workflow will use. Parameters allow you to change how the workflow behaves:
    
    - **Parameter Name**: A unique name for the parameter.  
    - **Parameter Type**: The type of value (String, Integer, Boolean, etc.).  
    - **Default Value**: The initial value, which you can modify later.  
    - **Description**: A short explanation of what the parameter does.
    
    **Example**:  
    - Parameter Name: `read_length`  
    - Type: `Integer`  
    - Default Value: `150`  
    - Description: `The length of reads in the sequencing data.`
    """
)
parameters = collect_parameters()

# Step 4: Environment Setup
st.markdown("### Step 4: Environment Setup")
st.markdown(
    """
    **What is this step?**  
    This step determines how the software and tools are managed in your workflow:
    
    - **Docker/Singularity**: Choose a container image to ensure consistent execution.  
    - **Conda**: Upload a Conda environment file for software management without containers.
    
    **Example**:  
    - Using Docker: `biocontainers/samtools:v1.9.0_cv4`
    """
)
containerization = st.selectbox(
    "Container Option", ["None", "Docker", "Singularity", "Conda"]
)
environment = {"container": containerization}
if containerization == "Docker":
    environment["docker_image"] = st.text_input("Docker Image Name")
elif containerization == "Conda":
    conda_file = st.file_uploader("Upload Conda Environment YAML")
    if conda_file:
        environment["conda_file_name"] = conda_file.name

# Step 5: Output Configuration
st.markdown("### Step 5: Output Configuration")
st.markdown(
    """
    **What is this step?**  
    This step configures the output of the workflow:
    
    - **Output Directory**: Where the results should be saved.  
    - **Generate Debug Logs**: Whether to generate additional log files for debugging.  
    - **File Naming Pattern**: A pattern for naming the output files.
    
    **Example**:  
    - Output Directory: `results/`  
    - Generate Debug Logs: `Yes`  
    - File Naming Pattern: `sample_{sample_id}.txt`
    """
)
output_config = {
    "output_dir": st.text_input("Output Directory"),
    "generate_logs": st.checkbox("Generate Debug Logs"),
    "file_naming": st.text_input("Result File Naming Pattern (Optional)"),
}

# Step 6: Process Steps Definition
st.markdown("### Step 6: Process Steps Definition")
st.markdown(
    """
    **What is this step?**  
    Define the tasks (processes) that make up your workflow:
    
    - **Process Name**: The name of the task.  
    - **Command**: The specific command to be executed.  
    - **Input Files**: Files needed for the command.  
    - **Output Files**: Expected output files from the command.
    
    **Example**:  
    - Process Name: `align_reads`  
    - Command: `bwa mem -t 8 ref.fa sample.fastq > aligned.bam`  
    - Input Files: `ref.fa, sample.fastq`  
    - Output Files: `aligned.bam`
    """
)
processes = collect_processes()

# Step 7: Additional Configurations
st.markdown("### Step 7: Additional Configurations")
st.markdown(
    """
    **What is this step?**  
    Here, you can specify advanced configurations like using a cluster scheduler for running the workflow:
    
    - **Scheduler**: Choose a scheduler like SLURM if running on a cluster.  
    - **Queue Name**: The name of the queue (if applicable).
    
    **Example**:  
    - Scheduler: `SLURM`  
    - Queue Name: `bioinformatics_queue`
    """
)
scheduler = {
    "scheduler": st.selectbox("Scheduler (Cluster)", ["None", "SLURM", "SGE"]),
    "queue": st.text_input("Queue Name (If Applicable)"),
}

# Preview & Download
st.header("Preview & Download")
if st.button("Generate Nextflow File"):
    nextflow_content = generate_nextflow_file(
        project_info=project_info,
        parameters=parameters,
        processes=processes,
        environment=environment,
        output_config=output_config,
        scheduler=scheduler,
    )
    st.text_area("Nextflow File Preview", value=nextflow_content, height=300)
    st.download_button(
        "Download Nextflow File", data=nextflow_content, file_name="workflow.nf"
    )
