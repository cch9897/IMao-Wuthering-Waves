using System.Globalization;
using System.Reflection;
using System.Text.Json;
using CommunityToolkit.WinUI.Controls;
using IMao_WinUI.Helpers;
using IMao_WinUI.StringItems;
using IMao_WinUI.ViewModels;
using Microsoft.UI;
using Microsoft.UI.Text;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Media;
using Microsoft.UI.Xaml.Shapes;
namespace IMao_WinUI.Views;

public sealed partial class FilterPage : Page
{
    private readonly StringItem stringItem = new StringItem();
    private LocalItemFilter localItemFilter = new LocalItemFilter();
    public FilterViewModel ViewModel
    {
        get;
    }

    public FilterPage()
    {
        ViewModel = App.GetService<FilterViewModel>();
        InitializeComponent();

        stringItem.LoadString(language.Text);
        GenerateCheckBoxes();
    }

    private void GenerateCheckBoxes()
    {
        var filteredItemsDatas = localItemFilter.GetFilteredItemsDatas();
        foreach (var itemsDatas in stringItem.itemsDatas)
        {
            String category = itemsDatas.Category;

            // 分组标题 + 可折叠
            var expander = new Expander
            {
                Header = category,
                IsExpanded = true,
                HorizontalAlignment = HorizontalAlignment.Stretch,
                HorizontalContentAlignment = HorizontalAlignment.Stretch
            };

            var panel = new WrapPanel
            {
                Orientation = Orientation.Horizontal,
                HorizontalAlignment = HorizontalAlignment.Left
            };

            foreach (var itemDatas in itemsDatas.ItemDatas)
            {
                bool isChecked = false;
                foreach(var filteredItemDatas in filteredItemsDatas)
                {
                    if (filteredItemDatas.Name == itemDatas.Id && filteredItemDatas.Status == 1)
                    {
                        isChecked = true;
                    }
                }

                CheckBox checkBox = new CheckBox
                {
                    Content = itemDatas.Name_SpecifiedLanguage,
                    Margin = new Thickness(20, 4, 0, 0),
                    FontSize = 14,
                    IsChecked = isChecked,
                    HorizontalAlignment = HorizontalAlignment.Left
                };

                checkBox.Checked += CheckBox_CheckedChanged;
                checkBox.Unchecked += CheckBox_CheckedChanged;

                panel.Children.Add(checkBox);
            }

            expander.Content = panel;
            GroupContainer.Children.Add(expander);
        }
    }

    private void CheckBox_CheckedChanged(object sender, RoutedEventArgs e)
    {
        CheckBox checkBox = sender as CheckBox;
        if (checkBox != null)
        {
            String itemId = stringItem.GetItemID(checkBox.Content.ToString());
            if(itemId != null)
            {
                if ((bool)checkBox.IsChecked)
                {
                    IMaoCoreAPI.AddItem(itemId);
                    localItemFilter.SetItmeFilterStatus(itemId, 1);
                }
                else
                {
                    IMaoCoreAPI.ClearItem(itemId);
                    localItemFilter.SetItmeFilterStatus(itemId, 0);
                }
            }
        }
    }

}
