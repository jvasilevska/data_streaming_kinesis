class EventMapper:
    PROP_ID="id"
    PROP_AGGREGATE_ID="aggregate_id"
    PROP_TYPE="type"
    PROP_TIMESTAMP="timestamp"
    PROP_DATA="data"
    PROP_NAME="name"
    PROP_BIRTHDATE="birthdate"

    VAL_TYPE_CUST_REG = "customer_registered"
    VAL_TYPE_PROD_ORD = "product_ordered"

    @staticmethod
    def json_to_csv_row(item):
        csv_row_list = []
        csv_row_list.append(item.get(EventMapper.PROP_ID))
        csv_row_list.append(item.get(EventMapper.PROP_AGGREGATE_ID))
        csv_row_list.append(item.get(EventMapper.PROP_TYPE))
        csv_row_list.append(item.get(EventMapper.PROP_TIMESTAMP))
        if item.get(EventMapper.PROP_TYPE) == EventMapper.VAL_TYPE_CUST_REG:
            csv_row_list.append(item.get(EventMapper.PROP_DATA).get(EventMapper.PROP_NAME)[0])
            csv_row_list.append(item.get(EventMapper.PROP_DATA).get(EventMapper.PROP_BIRTHDATE))
            csv_row_list.append("")
        elif item.get(EventMapper.PROP_TYPE) == EventMapper.VAL_TYPE_PROD_ORD:
            csv_row_list.append("")
            csv_row_list.append("")
            csv_row_list.append(item.get(EventMapper.PROP_DATA).get(EventMapper.PROP_NAME))
        else:
            csv_row_list.append("")
            csv_row_list.append("")
            csv_row_list.append("")

        return (",".join(csv_row_list)+'\n').encode('utf-8')
