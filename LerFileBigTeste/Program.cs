using MySql.Data.MySqlClient;
using System.Data;
using System.Diagnostics;
using System.IO;
using System.Text;

internal class Program
{
    private static void Main(string[] args)
    {
        string path = @"C:\gldo\ale\resultados.csv";

        string ConnectionString = "server=177.234.152.114;Uid=deltafox_gulopes;Pwd=Eumamomeuirmaozinho;Database=deltafox_api_datasus";

        StringBuilder sCommand = new StringBuilder("INSERT INTO deltafox_api_datasus.dbSUS (cpf,pai,mae,municipio_nasci,endereco_muni,endereco_logr,endereco_num,endereco_ba,endereco_ce,rg_numero,rg_orgao_emi,rg_uf,rg_data_emissao,cns,telefone) VALUES ");
        List<string> Rows = new List<string>();
        int linhas = 0;

        using (var mConnection = new MySqlConnection(ConnectionString))
        {

            mConnection.Open();

            MySqlTransaction transaction = mConnection.BeginTransaction();

            StreamReader r = new StreamReader(path);
            while (!r.EndOfStream)  //This is a little cleaner to my eyes
            {
                string line = r.ReadLine();
                linhas += 1;
                if (line != null)
                {
                    string[] campos = line.Split(new char[] { ',' });

                    if (campos.Length > 0)
                    {
                        string cpf = string.Empty,
                                pai = string.Empty,
                                mae = string.Empty,
                                municipioNasci = string.Empty,
                                enderecoMuni = string.Empty,
                                enderecoLogr = string.Empty,
                                enderecoNu = string.Empty,
                                enderecoBa = string.Empty,
                                enderecoCe = string.Empty,
                                rgNumero = string.Empty,
                                rgOrgaoEmi = string.Empty,
                                rgUf = string.Empty,
                                rgDataEmissao = string.Empty,
                                cns = string.Empty,
                                telefone = string.Empty;

                        cpf = campos[0].Replace("'", "");
                        if (campos.Length > 1) { pai = campos[1].Replace("'", ""); }
                        if (campos.Length > 2) { mae = campos[2].Replace("'", ""); }
                        if (campos.Length > 3) { municipioNasci = campos[3].Replace("'", ""); }
                        if (campos.Length > 4) { enderecoMuni = campos[4].Replace("'", ""); }
                        if (campos.Length > 5) { enderecoLogr = campos[5].Replace("'", ""); }
                        if (campos.Length > 6) { enderecoNu = campos[6].Replace("'", ""); }
                        if (campos.Length > 7) { enderecoBa = campos[7].Replace("'", ""); }
                        if (campos.Length > 8) { enderecoCe = campos[8].Replace("'", ""); }
                        if (campos.Length > 9) { rgNumero = campos[9].Replace("'", ""); }
                        if (campos.Length > 10) { rgOrgaoEmi = campos[10].Replace("'", ""); }
                        if (campos.Length > 11) { rgUf = campos[11].Replace("'", ""); }
                        if (campos.Length > 12) { rgDataEmissao = campos[12].Replace("'", ""); }
                        if (campos.Length > 13) { cns = campos[13].Replace("'", ""); }
                        if (campos.Length > 14) { telefone = campos[14].Replace("'", ""); }

                        Rows.Add(string.Format("('{0}','{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}')",
                            MySqlHelper.EscapeString(cpf),
                            MySqlHelper.EscapeString(pai),
                            MySqlHelper.EscapeString(mae),
                            MySqlHelper.EscapeString(municipioNasci),
                            MySqlHelper.EscapeString(enderecoMuni),
                            MySqlHelper.EscapeString(enderecoLogr),
                            MySqlHelper.EscapeString(enderecoNu),
                            MySqlHelper.EscapeString(enderecoBa),
                            MySqlHelper.EscapeString(enderecoCe),
                            MySqlHelper.EscapeString(rgNumero),
                            MySqlHelper.EscapeString(rgOrgaoEmi),
                            MySqlHelper.EscapeString(rgUf),
                            MySqlHelper.EscapeString(rgDataEmissao),
                            MySqlHelper.EscapeString(cns),
                            MySqlHelper.EscapeString(telefone)));

                    }
                }

                if (linhas % 100000 == 0 && linhas < 184377364)
                {
                    Rows.Clear();
                    Console.WriteLine("Inserindo até linha: " + linhas + "/184377364 - Falta:" + (184377364 - linhas).ToString());
                }

                if (linhas >= 184377364)
                {
                    try
                    {
                        if(mConnection.State != ConnectionState.Open)
                        {
                            mConnection.Open();
                        }

                        Console.WriteLine("Inserindo até linha: " + linhas + "/184377364 - Falta:" + (184377364 - linhas).ToString());
                        sCommand = new StringBuilder("INSERT INTO deltafox_api_datasus.dbSUS (cpf,pai,mae,municipio_nasci,endereco_muni,endereco_logr,endereco_num,endereco_ba,endereco_ce,rg_numero,rg_orgao_emi,rg_uf,rg_data_emissao,cns,telefone) VALUES ");
                        sCommand.Append(string.Join(",", Rows));
                        sCommand.Append(";");

                        using (MySqlCommand myCmd = new MySqlCommand(sCommand.ToString(), mConnection))
                        {
                            myCmd.CommandType = CommandType.Text;
                            myCmd.ExecuteNonQuery();
                        }

                        Rows.Clear();
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine(ex.ToString());
                    }
                }
            }
        }
    
    }
}