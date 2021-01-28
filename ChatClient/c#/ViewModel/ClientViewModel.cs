using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Net.Sockets;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Controls;
using System.Windows.Input;
using chatClient.Annotations;

namespace chatClient.ViewModel
{
    public class ClientViewModel : ICommand, INotifyPropertyChanged
    {

        private Socket client;

        private bool connected;

        public bool Connected
        {
            get => this.connected;
            set
            {
                this.connected = value;
                OnPropertyChanged();
            }
        }

        public AsyncObservableCollection<string> Messages { get; set; } = new AsyncObservableCollection<string>();

        public bool CanExecute(object? parameter)
        {
            return true;
        }

        public void Execute(object? parameter)
        {
            if (parameter is object[] parameters)
            {

                if (!(parameters[0] is string operation))
                    return;

                if (operation == "connect")
                {
                    var address = (string) parameters[1];
                    int.TryParse((string) parameters[2], out var port);
                    var nick = (string) parameters[3];

                    ConnectSocket(address, port, nick);
                }
            }
            else if (parameter is string param)
            {
                if (param == "disconnect")
                    DisconnectSocket();

            }
            else if (parameter is TextBox tb)
            {
                SendMessage(tb.Text);
                tb.Text = "";
            }

        }

        public event EventHandler? CanExecuteChanged;


        private void ConnectSocket(string address, int port, string nick)
        {
            client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            try
            {
                client.Connect(address, port);
                this.Connected = true;
                this.Messages.Add($"Connected to {address}:{port}");
            }
            catch
            {
                this.Messages.Add($"Coludn't connect to {address}:{port}");
                return;
            }

            var b = Encoding.UTF8.GetBytes($"nick {nick}");

            client.Send(b);

            Task.Factory.StartNew(RecMessages);

        }

        private void DisconnectSocket()
        {
            client.Disconnect(false);
            client.Close();
            client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        }

        private void SendMessage(string message)
        {
            this.Messages.Add($"<You> {message}");
            try
            {
                var b = Encoding.UTF8.GetBytes(message);
                this.client.Send(b);
            }
            catch (Exception)
            {
                this.Connected = false;
                this.Messages.Add($"You disconnected from {this.client.RemoteEndPoint}");
            }
        }


        private void RecMessages()
        {
            try
            {
                while (true)
                {
                    var b = new byte[2048];
                    this.client.Receive(b);

                    var message = Encoding.UTF8.GetString(b);


                    if (string.IsNullOrWhiteSpace(message))
                        return;

                    this.Messages.Add(message);

                }
            }
            catch (Exception)
            {
                client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                this.Connected = false;
            }
        }

        public event PropertyChangedEventHandler? PropertyChanged;

        [NotifyPropertyChangedInvocator]
        protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
