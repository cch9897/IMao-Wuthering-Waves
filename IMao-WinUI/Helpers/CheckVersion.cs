using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

namespace IMao_WinUI.Helpers;

class CheckVersion
{
    // 更新通道指向本 fork（含 3.5 数据/梦州地图/过滤器重构等增强）
    private static readonly String CurrentVersion = "v2-full";
    public static async Task<bool> IsLatest()
    {
        String tagName = await GetLatestTagName();
        if (!String.IsNullOrEmpty(tagName))
        {
            if (tagName == CurrentVersion)
            {
                return true;
            }
            return false;
        }
        else
        {
            return true;
        }
    }

    static async Task<String> GetLatestTagName()
    {
        String apiUrl = "https://api.github.com/repos/cch9897/IMao-Wuthering-Waves/releases/latest";

        using (var httpClient = new HttpClient { Timeout = TimeSpan.FromSeconds(8) })
        {
            try
            {
                httpClient.DefaultRequestHeaders.UserAgent.ParseAdd("MyC#App/1.0");

                var response = await httpClient.GetAsync(apiUrl);

                if (response.IsSuccessStatusCode)
                {
                    String json = await response.Content.ReadAsStringAsync();

                    JObject jsonObject = JObject.Parse(json);
                    return jsonObject["tag_name"]?.ToString();
                }
            }
            catch (TaskCanceledException)
            {
                Console.WriteLine("请求超时，已跳过");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"发生错误: {ex.Message}");
            }
        }

        return null;
    }
}