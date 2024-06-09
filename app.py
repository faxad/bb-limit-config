import json
import pandas as pd

from jinja2 import Template

template = Template('''{% for (FUN, LIMIT) in CONFIG %}{% if FUN != 'FAG' %}
  {
    "user-BBID": "user_backbase_id",
    "entities": [
      {
        "etype": "FUN",
        "eref": "{{FUN}}"
      },
      {
        "etype": "FAG",
        "eref": "{{FAG_NAME}}"
      },
      {
        "etype": "SA",
        "eref": "service_agreement"
      },
      {
        "etype": "PRV",
        "eref": "approve"
      }
    ],
    "shadow": false,
    "currency": "SAR",
    "periodic-limits-bounds": {
      "daily": "{{LIMIT}}",
      "customPeriods": []
    }
  },{% endif %}{% endfor %}''')


def main():
    df = pd.read_excel("limits.xlsx")
    fag_lookup = pd.read_excel(
        "limits.xlsx",
        sheet_name="function_group"
    ).set_index('Name')['FAG_ID'].to_dict()
    
    df['FAG'] = df['FAG'].map(fag_lookup)

    fun_lookup = pd.read_excel(
        "limits.xlsx",
        sheet_name="business_function"
    ).set_index('Name')['Code'].astype(str).to_dict()

    df.columns = df.columns.map(fun_lookup).fillna("FAG")

    result = ""

    for loc in df.iloc:
        config = loc.to_dict()
        result += template.render(CONFIG = config.items(), FAG_NAME = config['FAG'])

    sas = pd.read_excel(
        "limits.xlsx",
        sheet_name="service_agreement_user"
    ).to_dict("records")

    for sa in sas:
        output = json.loads(
            "[" + result.replace("service_agreement", sa["SA_ID"]).replace("user_backbase_id", sa["USER_ID"])[:-1] + "]")
            
        with open("payload/request/" + sa["USER_ID"]+'.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()

