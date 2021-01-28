using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Printing.IndexedProperties;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Data;

namespace chatClient.ViewModel
{
    public class CommandParamConverter : IMultiValueConverter
    {
        public object Convert(object[] values, Type targetType, object parameter, CultureInfo culture)
        {
            if (values.Length == 3)
                return new object[]{"connect", values[0], values[1], values[2]};
            if (values.Length == 1)
                return values[0];
            return null;
        }

        public object[] ConvertBack(object value, Type[] targetTypes, object parameter, CultureInfo culture)
        {
            return null;
        }
    }
}
