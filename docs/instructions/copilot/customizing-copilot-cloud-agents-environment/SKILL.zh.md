---
名称：定制-copilot-云-代理-环境
描述：>-
    自定义 Copilot 云代理（以前称为 Copilot 编码代理）环境的指南，
    包括 copilot-setup-steps.yml 配置、预安装工具和依赖项、运行程序和设置。
用户可调用：true
---

# 自定义 GitHub Copilot 云代理的开发环境

了解如何使用其他工具自定义 GitHub Copilot 的开发环境。

## 关于自定义 Copilot 云代理的开发环境

在执行任务时，Copilot 可以访问由 GitHub Actions 提供支持的自己的临时开发环境，可以在其中探索代码、进行更改、执行自动化测试和 linter 等。

您可以使用 [Copilot 设置步骤文件](#customizing-copilots-development-environment-with-copilot-setup-steps) 自定义 Copilot 的开发环境。您可以使用 Copilot 设置步骤文件来：

- [在 Copilot 环境中预安装工具或依赖项](#preinstalling-tools-or-dependencies-in-copilots-environment)
- [从标准 GitHub 托管的 GitHub Actions 运行器升级到更大的运行器](#upgrading-to-larger-github-hosted-github-actions-runners)
- [在 GitHub Actions 自托管运行器上运行](#using-self-hosted-github-actions-runners)
- [为 Copilot 提供 Windows 开发环境](#switching-copilot-to-a-windows-development-environment)，而不是默认的 Ubuntu Linux 环境
- [启用 Git 大文件存储 (LFS)](#enabling-git-large-file-storage-lfs)

此外，您还可以：

- [在 Copilot 环境中设置环境变量](#setting-environment-variables-in-copilots-environment)
- [禁用或自定义代理的防火墙](https://docs.github.com/en/enterprise-cloud@latest/copilot/customizing-copilot/customizing-or-disabling-the-firewall-for-copilot-coding-agent)。

## 使用 Copilot 设置步骤自定义 Copilot 的开发环境

您可以通过创建特殊的 GitHub Actions 工作流程文件来自定义 Copilot 的环境，该文件位于存储库中的“.github/workflows/copilot-setup-steps.yml”。“copilot-setup-steps.yml” 文件看起来像普通的 GitHub Actions 工作流程文件，但必须包含单个“copilot-setup-steps” 作业。该作业中的步骤将在 Copilot 开始工作之前在 GitHub Actions 中执行。有关 GitHub Actions 工作流文件的更多信息，请参阅 [GitHub Actions 的工作流语法](https://docs.github.com/en/enterprise-cloud@latest/actions/using-workflows/workflow-syntax-for-github-actions)。

> [!注意]
> “copilot-setup-steps.yml”工作流程不会触发，除非它存在于您的默认分支上。

以下是 TypeScript 项目的“copilot-setup-steps.yml”文件的简单示例，该文件克隆项目、安装 Node.js 并下载和缓存项目的依赖项。您应该自定义它以适合您自己项目的语言和依赖项：

@@代码块0@@

在“copilot-setup-steps.yml”文件中，您只能自定义“copilot-setup-steps”作业的以下设置。如果您尝试自定义其他设置，您的更改将被忽略。

- `步骤`（见上文）
- `权限`（见上文）
- `runs-on`（见下文）
- `服务`
- `快照`
- `超时分钟数`（最大值：`59`）

有关这些选项的更多信息，请参阅 [GitHub Actions 的工作流语法](https://docs.github.com/en/enterprise-cloud@latest/actions/writing-workflows/workflow-syntax-for-github-actions#jobs)。

为“actions/checkout”操作的“fetch-深度”选项设置的任何值都将被覆盖，以允许代理根据请求回滚提交，同时降低安全风险。有关更多信息，请参阅 [`actions/checkout/README.md`](https://github.com/actions/checkout/blob/main/README.md)。

进行更改时，您的“copilot-setup-steps.yml”文件将作为正常的 GitHub Actions 工作流程自动运行，以便您可以查看它是否成功运行。这将与您创建或修改文件的拉取请求中的其他检查一起显示。

将 yml 文件合并到默认分支后，您可以随时从存储库的 **Actions** 选项卡手动运行工作流程，以检查一切是否按预期运行。有关更多信息，请参阅[手动运行工作流](https://docs.github.com/en/enterprise-cloud@latest/actions/managing-workflow-runs-and-deployments/managing-workflow-runs/manually-running-a-workflow)。当 Copilot 开始工作时，您的设置步骤将运行，并且更新将显示在会话日志中。请参阅[跟踪 GitHub Copilot 的会话](https://docs.github.com/en/enterprise-cloud@latest/copilot/how-tos/agents/copilot-coding-agent/tracking-copilots-sessions)。

如果任何设置步骤因返回非零退出代码而失败，Copilot 将跳过剩余的设置步骤并开始使用其开发环境的当前状态。

## 在 Copilot 环境中预安装工具或依赖项

在其临时开发环境中，Copilot 可以构建或编译您的项目并运行自动化测试、linter 和其他工具。为此，需要安装项目的依赖项。

Copilot 可以通过反复试验的过程自行发现并安装这些依赖项，但考虑到大型语言模型 (LLM) 的不确定性，这可能会很慢且不可靠，并且在某些情况下，它可能完全无法下载这些依赖项（例如，如果它们是私有的）。

您可以使用 Copilot 设置步骤文件在 Copilot 开始工作之前确定性地安装工具或依赖项。为此，请将“steps”添加到“copilot-setup-steps”作业中：

@@代码块1@@

## 升级到更大的 GitHub 托管的 GitHub Actions 运行器

默认情况下，Copilot 在标准 GitHub Actions 运行器中工作。您可以升级到更大的运行程序以获得更好的性能（CPU 和内存）、更多磁盘空间和 Azure 专用网络等高级功能。有关更多信息，请参阅[大型运行程序](https://docs.github.com/en/enterprise-cloud@latest/actions/using-github-hosted-runners/using-larger-runners/about-larger-runners)。

1. 为您的组织设置更大的跑步者。有关更多信息，请参阅[管理大型运行程序](https://docs.github.com/en/enterprise-cloud@latest/actions/using-github-hosted-runners/managing-larger-runners)。2. 如果您在 Azure 专用网络中使用较大的运行器，请配置您的 Azure 专用网络以允许对 Copilot 云代理所需的主机进行出站访问：
    - `uploads.github.com`
    - `user-images.githubusercontent.com`
    - `api.individual.githubcopilot.com`（如果您希望 Copilot Pro 或 Copilot Pro+ 用户在您的存储库中使用 Copilot 云代理）
    - `api.business.githubcopilot.com`（如果您希望 Copilot Business 用户在您的存储库中使用 Copilot 云代理）
    - `api.enterprise.githubcopilot.com`（如果您希望 Copilot Enterprise 用户在您的存储库中使用 Copilot 云代理）
    - 如果您使用的是 OpenAI Codex 第三方代理（有关更多信息，请参阅[关于第三方代理](https://docs.github.com/en/enterprise-cloud@latest/copilot/concepts/agents/about-third-party-agents)）：
        - `npmjs.org`
        - `npmjs.com`
        - `registry.npmjs.com`
        - `registry.npmjs.org`
        - `skimdb.npmjs.com`

3. 使用存储库中的“copilot-setup-steps.yml”文件将 Copilot 云代理配置为在您选择的运行器上运行。将“copilot-setup-steps”作业的“runs-on”步骤设置为您希望 Copilot 使用的较大跑步者的标签和/或组。有关使用“runs-on”指定较大运行器的更多信息，请参阅[在较大运行器上运行作业](https://docs.github.com/en/enterprise-cloud@latest/actions/using-github-hosted-runners/running-jobs-on-larger-runners)。

    @@代码块2@@

> [!注意]
>
> - Copilot 云代理仅与 Ubuntu x64 Linux 和 Windows 64 位运行程序兼容。不支持 macOS 或其他操作系统的运行程序。

## 使用自托管的 GitHub Actions 运行器

您可以在自托管运行器上运行 Copilot 云代理。您可能希望执行此操作以匹配您在 GitHub Actions 上运行 CI/CD 工作流程的方式，或者允许 Copilot 访问网络上的内部资源。

我们建议您仅将 Copilot 云代理与不会重复用于多个作业的临时、一次性运行程序一起使用。大多数客户使用 ARC（Actions Runner 控制器）或 GitHub Actions Runner 规模集客户端进行设置。有关更多信息，请参阅[自托管运行器参考](https://docs.github.com/en/enterprise-cloud@latest/actions/reference/runners/self-hosted-runners#supported-autoscaling-solutions)。

> [!注意]
> Copilot 云代理仅兼容 Ubuntu x64 和 Windows 64 位运行程序。不支持 macOS 或其他操作系统的运行程序。1. 为 GitHub Actions 运行器配置网络安全控制，以确保 Copilot 云代理无法公开访问您的网络或公共互联网。

    您必须将防火墙配置为允许连接到 [GitHub Actions 自托管运行器所需的标准主机](https://docs.github.com/en/enterprise-cloud@latest/actions/reference/runners/self-hosted-runners#accessible-domains-by-function)，以及以下主机：
    - `uploads.github.com`
    - `user-images.githubusercontent.com`
    - `api.individual.githubcopilot.com`（如果您希望 Copilot Pro 或 Copilot Pro+ 用户在您的存储库中使用 Copilot 云代理）
    - `api.business.githubcopilot.com`（如果您希望 Copilot Business 用户在您的存储库中使用 Copilot 云代理）
    - `api.enterprise.githubcopilot.com`（如果您希望 Copilot Enterprise 用户在您的存储库中使用 Copilot 云代理）
    - 如果您使用的是 OpenAI Codex 第三方代理（有关更多信息，请参阅[关于第三方代理](https://docs.github.com/en/enterprise-cloud@latest/copilot/concepts/agents/about-third-party-agents)）：
        - `npmjs.org`
        - `npmjs.com`
        - `registry.npmjs.com`
        - `registry.npmjs.org`
        - `skimdb.npmjs.com`

2. 在存储库设置中禁用 Copilot 云代理的集成防火墙。防火墙与自托管运行器不兼容。除非禁用此选项，否则将阻止使用 Copilot 云代理。有关更多信息，请参阅[自定义或禁用 GitHub Copilot 云代理的防火墙](https://docs.github.com/en/enterprise-cloud@latest/copilot/customizing-copilot/customizing-or-disabling-the-firewall-for-copilot-coding-agent)。

3. 在“copilot-setup-steps.yml”文件中，将“runs-on”属性设置为 ARC 管理的规模集名称：

    @@代码块3@@

4. 如果要为 Copilot 云代理连接到互联网配置代理服务器，请根据需要配置以下环境变量：|变量|描述 |示例|
    | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
    | `https_proxy` | HTTPS 流量的代理 URL。如果需要，您可以包含基本身份验证。                                                                                                          | `http://proxy.local`<br>`http://192.168.1.1:8080`<br>`http://用户名:密码@proxy.local` |
    | `http_proxy` | HTTP 流量的代理 URL。如果需要，您可以包含基本身份验证。                                                                                                           | `http://proxy.local`<br>`http://192.168.1.1:8080`<br>`http://用户名:密码@proxy.local` |
    | `无代理` |应绕过代理的主机或 IP 地址的逗号分隔列表。有些客户端仅在直接连接到 IP 而不是主机名时才认可 IP 地址。 | `example.com`<br>`example.com,myserver.local:443,example.org` |
    | `ssl_cert_file` |代理服务器提供的 SSL 证书的路径。如果您的代理拦截 SSL 连接，您将需要配置此项。                                               | `/path/to/key.pem` |
    | `node_extra_ca_certs` |代理服务器提供的 SSL 证书的路径。如果您的代理拦截 SSL 连接，您将需要配置此项。                                               | `/path/to/key.pem` |您可以按照[下面的说明](#setting-environment-variables-in-copilots-environment) 设置这些环境变量，或者直接在运行器上设置它们，例如使用自定义运行器图像。有关构建自定义映像的更多信息，请参阅 [Actions Runner Controller](https://docs.github.com/en/enterprise-cloud@latest/actions/concepts/runners/actions-runner-controller#creating-your-own-runner-image)。

## 将 Copilot 切换到 Windows 开发环境

默认情况下，Copilot 使用基于 Ubuntu Linux 的开发环境。

如果您正在为 Windows 构建软件，或者您的存储库使用基于 Windows 的工具链，则您可能需要使用 Windows 开发环境，以便 Copilot 可以构建您的项目、运行测试并验证其工作。

Copilot 云代理的集成防火墙与 Windows 不兼容，因此我们建议您仅使用自托管运行器或具有 Azure 专用网络的大型 GitHub 托管运行器，您可以在其中实现自己的网络控制。有关使用 Azure 专用网络的运行器的详细信息，请参阅[关于企业中 GitHub 托管运行器的 Azure 专用网络](https://docs.github.com/en/enterprise-cloud@latest/admin/configuring-settings/configuring-private-networking-for-hosted-compute-products/about-azure-private-networking-for-github-hosted-runners-in-your-enterprise)。

要将 Windows 与自托管运行器结合使用，请按照上面的[使用自托管 GitHub Actions 运行器](#using-self-hosted-github-actions-runners) 部分中的说明操作，并使用 Windows 运行器的标签。要将 Windows 与较大的 GitHub 托管运行器结合使用，请按照上面的[升级到较大的运行器](#upgrading-to-larger-github-hosted-github-actions-runners) 部分中的说明操作，并使用 Windows 运行器的标签。

## 启用 Git 大文件存储 (LFS)

如果您使用 Git 大文件存储 (LFS) 在存储库中存储大文件，则需要自定义 Copilot 的环境来安装 Git LFS 并获取 LFS 对象。

要启用 Git LFS，请将“actions/checkout”步骤添加到“copilot-setup-steps”作业中，并将“lfs”选项设置为“true”。

```yaml
# ...

jobs:
    copilot-setup-steps:
        runs-on: ubuntu-latest
        permissions:
            contents: read # for actions/checkout
        steps:
            - uses: actions/checkout@v5
              with:
                  lfs: true
```

## 在 Copilot 环境中设置环境变量

您可能需要在 Copilot 的环境中设置环境变量来配置或验证它有权访问的工具或依赖项。要为 Copilot 设置环境变量，请在“copilot”环境中创建 GitHub Actions 变量或密钥。如果该值包含敏感信息，例如密码或 API 密钥，则最好使用 GitHub Actions 密钥。

1. 在 GitHub 上，导航到存储库的主页。
2. 在您的存储库名称下，单击“**设置**”。如果您看不到“设置”选项卡，请选择“**更多**”下拉菜单，然后单击“**设置**”。
3. 在左侧边栏中，单击“**环境**”。
4. 单击“copilot”环境。
5. 要添加机密，请在“环境机密”下单击“**添加环境机密**”。要添加变量，请在“环境变量”下单击“**添加环境变量**”。
6. 填写“名称”和“值”字段，然后根据需要单击“**添加秘密**”或“**添加变量**”。

## 进一步阅读

- [自定义或禁用 GitHub Copilot 云代理的防火墙](https://docs.github.com/en/enterprise-cloud@latest/copilot/customizing-copilot/customizing-or-disabling-the-firewall-for-copilot-coding-agent)